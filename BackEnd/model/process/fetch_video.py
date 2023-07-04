import cv2 as cv
from model.joint.in_app_parameters import FRAME_PARAMETERS
from model.widespread.logger import Logger


class FetchVideo:
    def __init__(self, input_media):
        self.logging = Logger('fetch_video')
        self.__flip_enabled = True if input_media == 0 else False

        self.__video_capture = cv.VideoCapture(input_media)
        self.retrieve, self.frame = self.__video_capture.read()
        self.logging.info('Video connection successfully connected')

        self._scale_factor = FRAME_PARAMETERS['frame_size'] / self.__video_capture.get(cv.CAP_PROP_FRAME_WIDTH)
        if self._scale_factor < 1:
            self._frame_width = FRAME_PARAMETERS['frame_size']
            self._frame_height = int(self.__video_capture.get(cv.CAP_PROP_FRAME_HEIGHT) * self._scale_factor)
            self.__resize_enabled = True
        else:
            self._frame_width = int(self.__video_capture.get(cv.CAP_PROP_FRAME_WIDTH))
            self._frame_height = int(self.__video_capture.get(cv.CAP_PROP_FRAME_HEIGHT))
            self.__resize_enabled = False
        self.logging.info('Input media resizing status is set to :', self.__resize_enabled)

    def reading_frames(self, convert_to_gray=False, blurring=False):
        """this method insures whether video can be continued or not.
        also it convert frame to gray and provides denoised frame if enabled"""
        # read further frame
        self.retrieve, self.frame = self.__video_capture.read()

        if self.retrieve:
            # resize input data to desire size
            self.frame = cv.resize(src=self.frame, dsize=(0, 0), fx=self._scale_factor, fy=self._scale_factor) \
                if self.__resize_enabled else self.frame

            # if web cam uses set this parameter enable
            self.frame = cv.flip(src=self.frame, flipCode=90) if self.__flip_enabled else self.frame

            # convert any colour space to gray
            self.frame = cv.cvtColor(src=self.frame, code=cv.COLOR_BGR2GRAY) if convert_to_gray else self.frame

            # remove noise from image to increase algorithm accuracy
            self.frame = cv.medianBlur(src=self.frame, ksize=5) if blurring else self.frame

        return self.retrieve

    def frame_getter(self):
        return self.frame
