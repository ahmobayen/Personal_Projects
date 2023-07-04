from model.joint.in_app_parameters import FRAME_PARAMETERS, ALGORITHM_PARAMETERS, TRACKER_PARAMETERS
from model.joint.static_paths import path, TRAINING_PATH

from model.widespread.db_connection import SqlDatabaseConnection
from model.widespread.logger import Logger

import datetime
import numpy
import cv2 as cv


class DNNDetection:
    def __init__(self):
        self.logging = Logger('deep_network')
        self.logging.info('Initializing DNN Detection.')

        self.frame = numpy.ndarray

        # Flags (All Types are considered private)
        self.elements_position = []  # considered for detected elements
        self.elements_category = []  # considered for any detail needs to be displayed for an element
        self.elements_id = []  # assign an ID to detected elements
        self.elements_agg_info = {}  # all info about detected items in each frame
        self.elements_direction = {}  # considered for detected direction

        # initializing deep network
        self.__classes = open(path.join(TRAINING_PATH, 'coco.names')).read().strip().split('\n')
        self.__net = cv.dnn.readNetFromDarknet(cfgFile=path.join(TRAINING_PATH, 'yolov4-tiny.cfg'),
                                               darknetModel=path.join(TRAINING_PATH, 'yolov4-tiny.weights'))

        self.__net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)

        if cv.ocl.haveOpenCL():
            self.logging.info('OpenCL Support status: TRUE', '\n\tenabling OpenCL support ... ')
            cv.ocl.setUseOpenCL(True)
            self.__net.setPreferableTarget(cv.dnn.DNN_TARGET_OPENCL)
        else:
            self.logging.info('OpenCL Support status: FALSE')
            self.__net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
        self.__layer = self.__net.getLayerNames()
        self.__layer = [self.__layer[i[0] - 1] for i in self.__net.getUnconnectedOutLayers()]

        self.accuracy_performance_ratio = (608, 608) if ALGORITHM_PARAMETERS['accuracy_performance_ratio'] == 3 else \
            (320, 320) if ALGORITHM_PARAMETERS['accuracy_performance_ratio'] == 1 else (416, 416)

        try:
            self.multi_tracker = cv.MultiTracker_create()
        except cv.Error as error:
            self.logging.error('Tracking is not supported:', error)

        self.logging.info('DNN successfully initialized')

    def multi_object_detection(self, frame):
        """ Using YOLO deep learning algorithm to determine objects in each frame"""
        # releasing allocated lists from previous frames
        self.frame = frame
        self.elements_position.clear() if len(self.elements_position) != 0 else self.elements_position
        self.elements_id.clear() if len(self.elements_id) != 0 else self.elements_id
        self.elements_category.clear() if len(self.elements_category) != 0 else self.elements_category
        self.elements_agg_info.clear() if len(self.elements_agg_info) != 0 else None

        # init local variables
        boxes = []
        confidences = []
        class_ids = []
        elements = []
        texts = []

        # running deep learning algorithm to determine required objects
        self.__net.setInput(cv.dnn.blobFromImage(image=self.frame, scalefactor=1 / 255.0,
                                                 size=self.accuracy_performance_ratio, swapRB=True, crop=False))
        frame_result = numpy.vstack(self.__net.forward(self.__layer))

        for output in frame_result:
            scores = output[5:]
            class_id = numpy.argmax(scores)
            confidence = scores[class_id]
            if confidence > ALGORITHM_PARAMETERS['confidence_threshold']:
                x, y, w, h = output[:4] * numpy.array([self.frame.shape[1], self.frame.shape[0],
                                                       self.frame.shape[1], self.frame.shape[0]])
                boxes.append([int(x - w // 2), int(y - h // 2), int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

        indices = cv.dnn.NMSBoxes(boxes, confidences, ALGORITHM_PARAMETERS['confidence_threshold'],
                                  ALGORITHM_PARAMETERS['confidence_nms_threshold'])
        if len(indices) > 0:
            for i in indices.flatten():
                element = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
                elements.append(element)
                texts.append("{}: {:.4f}".format(self.__classes[class_ids[i]], confidences[i]))

        element_info = list(zip(elements, texts))
        element_info.sort(key=lambda mob_ayn: mob_ayn[0])
        for count, item in enumerate(element_info, 1):
            self.elements_position.append(item[0])
            self.elements_category.append(item[1])
            self.elements_agg_info[count] = [item[0], item[1]]

        if len(self.elements_position) != 0:
            self.logging.info(f'number of detected items in frame: {len(self.elements_position)}')

        return self.elements_agg_info

    def object_tracking_initialization(self, frame, elements_position):
        """Separated in purpose of possibility to make concurrent processing.
        requirements of this class is frame and detected elements which must be
        obtained by deep_network."""

        #  tracking parameters
        def tracker_type():
            tracker = cv.TrackerBoosting_create() if TRACKER_PARAMETERS == 'BOOSTING' else \
                cv.TrackerMIL_create() if TRACKER_PARAMETERS == 'MIL' else \
                cv.TrackerKCF_create() if TRACKER_PARAMETERS == 'KCF' else \
                cv.TrackerTLD_create() if TRACKER_PARAMETERS == 'TLD' else \
                cv.TrackerMedianFlow_create() if TRACKER_PARAMETERS == 'MEDIANFLOW' else \
                cv.TrackerMOMOSSE_create() if TRACKER_PARAMETERS == 'MOSSE' else \
                cv.TrackerGOTURN_create() if TRACKER_PARAMETERS == 'GOTURN' else \
                cv.TrackerCSRTcreate() if TRACKER_PARAMETERS == 'CSRT' else cv.TrackerKCF_create()
            return tracker

        self.multi_tracker = cv.MultiTracker_create()
        for element in elements_position:
            self.multi_tracker.add(tracker_type(), frame, element)

    def object_tracking(self, frame):
        """The main process of object tracking base on defined algorithm.
        this must be used after object_tracking_initialization() method which
        initialize multi tracking algorithm. """

        # get updated location of objects in subsequent frames
        self.elements_agg_info.clear() if len(self.elements_agg_info) == 0 else None
        success, update_position = self.multi_tracker.update(frame)
        for count, position in enumerate(update_position, 0):
            self.elements_position[count] = (int(position[0]), int(position[1]), int(position[2]), int(position[3]))
            self.elements_agg_info[count + 1] = [self.elements_position[count], self.elements_category[count]]

        return self.elements_agg_info

    def direction_detection(self):
        """detecting object direction"""

        def summarize_given_info(element):
            position, group = element[0], element[1]
            centroid = int(position[0] + 0.5 * position[2]), int(position[1] + 0.5 * position[3])
            group = element[1].split(":")
            return [centroid, group[0]]

        def area_detection(previous_frame_slice, current_frame_slice):
            for current_frame_element_counter in current_frame_slice:
                if current_frame_element_counter not in self.elements_direction.keys():
                    current_element = summarize_given_info(current_frame[current_frame_element_counter])
                    for previous_frame_element_counter in previous_frame_slice:
                        previous_element = summarize_given_info(frame[previous_frame_element_counter])

                        if current_element[1] == previous_element[1] and \
                                (abs(current_frame_element_counter - current_frame_element_counter) < 2):

                            x_movement = current_element[0][0] - previous_element[0][0]
                            y_movement = current_element[0][1] - previous_element[0][1]
                            if x_movement <= 5 * ALGORITHM_PARAMETERS['direction_sensitivity']:
                                x_direction = 'Right' if x_movement > ALGORITHM_PARAMETERS['direction_sensitivity'] \
                                    else 'Left' if x_movement < - ALGORITHM_PARAMETERS['direction_sensitivity'] else\
                                    'Still'
                            else:
                                continue

                            if y_movement <= 2 * ALGORITHM_PARAMETERS['direction_sensitivity']:
                                y_direction = 'Down' if y_movement > ALGORITHM_PARAMETERS['direction_sensitivity'] \
                                    else 'Up' if y_movement < - ALGORITHM_PARAMETERS['direction_sensitivity'] else \
                                    'Still'
                            else:
                                continue

                            cv.line(img=self.frame, pt1=current_element[0], pt2=previous_element[0],
                                    color=FRAME_PARAMETERS['frame_red'], thickness=FRAME_PARAMETERS['frame_thickness'])
                            direction = [x_direction, y_direction]
                            self.elements_direction[current_frame_element_counter] = direction
                            break

        # initialization parameters
        self.elements_direction.clear() if len(self.elements_direction) != 0 else self.elements_direction
        self.elements_history.append(self.elements_agg_info.copy())

        # direction algorithm
        element_history = self.elements_history.copy()
        if self.elements_history[-1] != self.elements_history[0]:
            current_frame = element_history.pop(-1)
            for frame in element_history:
                area_detection(frame, current_frame) if len(self.elements_direction) <= len(current_frame) else None

        print(self.elements_direction)
        print(self.elements_agg_info)

        print('direction detected:', len(self.elements_direction))

        # controlling validation of algorithm in continues situations
        if len(self.elements_history) == ALGORITHM_PARAMETERS['direction_frame_sensitivity']:
            self.elements_history.pop(0)

    def save_to_db(self):
        query_items = []
        db_connection = SqlDatabaseConnection()
        if self.elements_agg_info:
            for list_id, elements_data in self.elements_agg_info.items():
                current_time = datetime.datetime.now()
                try:
                    if self.elements_direction:
                        if list_id in self.elements_direction:
                            if str(self.elements_direction[id]) != "['Still', 'Still']":
                                query_items.append((list_id, elements_data[1], str(self.elements_direction[list_id]),
                                                    current_time.strftime("%Y-%m-%d %H:%M:%S")))

                    else:
                        query_items.append((list_id, elements_data[1], '-',
                                            current_time.strftime("%Y-%m-%d %H:%M:%S")))
                finally:
                    db_connection.commit_query('INSERT INTO passage(id, detected_type, direction, time)'
                                               'values (%s, %s, %s, %s)', query_items)
