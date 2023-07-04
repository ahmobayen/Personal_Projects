import cv2 as cv
import numpy as np


class CoordinatesGenerator:
    KEY_RESET = ord("r")
    KEY_QUIT = ord("q")

    def __init__(self, input_media, output):
        self.output = output
        self.caption = input_media
        self.color = (0, 0, 255)  # colour is Red

        try:
            self.image = cv.imread(input_media).copy()
        except:
            self.video_capture = cv.VideoCapture(input_media)
            self.retrieve, self.image = self.video_capture.read()

        self.click_count = 0
        self.ids = 0
        self.coordinates = []

        cv.namedWindow(self.caption, cv.WINDOW_GUI_EXPANDED)
        cv.setMouseCallback(self.caption, self.__mouse_callback)

    def generate(self):
        while True:
            cv.imshow(self.caption, self.image)
            key = cv.waitKey(0)

            if key == CoordinatesGenerator.KEY_RESET:
                self.image = self.image.copy()
            elif key == CoordinatesGenerator.KEY_QUIT:
                break
        cv.destroyWindow(self.caption)

    def __mouse_callback(self, event, x, y, flags, params):
        if event == cv.EVENT_LBUTTONDOWN:
            self.coordinates.append((x, y))
            self.click_count += 1

            if self.click_count >= 4:
                self.click_count = 0
                coordinates = np.array(self.coordinates)
                cv.line(self.image, self.coordinates[2], self.coordinates[3], self.color, 1)
                cv.line(self.image, self.coordinates[3], self.coordinates[0], self.color, 1)
                self.output.write("-\n          id: " + str(self.ids) + "\n          coordinates: [" +
                                  "[" + str(self.coordinates[0][0]) + "," + str(self.coordinates[0][1]) + "]," +
                                  "[" + str(self.coordinates[1][0]) + "," + str(self.coordinates[1][1]) + "]," +
                                  "[" + str(self.coordinates[2][0]) + "," + str(self.coordinates[2][1]) + "]," +
                                  "[" + str(self.coordinates[3][0]) + "," + str(self.coordinates[3][1]) + "]]\n")

                self.draw_contours(self.image, coordinates, str(self.ids + 1), (255, 0, 0))  # colour is Blue
                self.ids += 1
                self.coordinates.clear()

            elif self.click_count > 1:
                cv.line(self.image, self.coordinates[-2], self.coordinates[-1], (255, 0, 0), 1)

        cv.imshow(self.caption, self.image)

    @staticmethod
    def draw_contours(image, coordinates, label, font_color, border_color=(0, 0, 255), line_thickness=1,
                      font=cv.FONT_HERSHEY_SIMPLEX, font_scale=0.5):
        cv.drawContours(image, [coordinates], contourIdx=-1, color=border_color, thickness=2, lineType=cv.LINE_8)
        moments = cv.moments(coordinates)
        center = (int(moments["m10"] / moments["m00"]) - 3, int(moments["m01"] / moments["m00"]) + 3)
        cv.putText(image, label, center, font, font_scale, font_color, line_thickness, cv.LINE_AA)
