
from model.joint.in_app_parameters import FRAME_PARAMETERS
import cv2 as cv
import numpy


class Display:
    def __init__(self):
        self.frame = numpy.ndarray

    def frame_setter(self, frame):
        """set the input frame for process."""
        self.frame = frame

    def add_object_to_display(self, elements_agg_info, elements_direction):
        """displays current frame to external window or web whether detection and tracking algorithms run or not
        if there is detected item it will add it to frame and display it"""
        try:
            for ids in elements_agg_info:
                element = elements_agg_info[ids]
                position = element[0]
                text = element[1]
                cv.rectangle(self.frame, (position[0], position[1]),
                             (position[0] + position[2], position[1] + position[3]),
                             (255, 255, 255), FRAME_PARAMETERS['frame_thickness'])

                cv.putText(self.frame, text, (position[0], position[1] - 5),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                           FRAME_PARAMETERS['frame_thickness']) if text else None

                if ids in elements_direction:
                    direction = str(elements_direction[ids])
                    cv.putText(self.frame, direction, (position[0], position[1] + 10),
                               cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                               FRAME_PARAMETERS['frame_thickness'])
        finally:
            pass

    def display_frames(self):
        """show given frame in windows."""
        cv.imshow('frame', self.frame)

    def frame_to_stream(self):
        """convert given frame to byte. it considered for web usage"""
        ret, jpeg = cv.imencode('.jpg', self.frame)
        return jpeg.tobytes()

    def save_to_file(self):
        cv.imwrite('process', self.frame)

