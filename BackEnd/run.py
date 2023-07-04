import json
import time
from model.joint.in_app_parameters import CCTV_CONNECTION
from model.process.fetch_video import FetchVideo
from model.process.cctv_connection import CheckConnection
import model.process.video_results as video
import model.process.deep_learning as detection
import threading
import queue
from model.socket_server_side import SocketServerSide, video_request, elements_request
# enable if uses OpenCv-contrib-python
# import cv2 as cv


stream_queue = queue.Queue()


def frame_grabber():
    connection = CheckConnection(CCTV_CONNECTION)
    grab_video = FetchVideo(connection.check_connection())
    while grab_video.reading_frames():
        stream_queue.put(grab_video.frame_getter())


def result():
    deep = detection.DNNDetection()
    display = video.Display()
    while True:
        start_time = time.time()
        if not stream_queue.empty():
            frame = stream_queue.get()
            detected_elements = deep.multi_object_detection(frame)
            display.frame_setter(frame)
            display.add_object_to_display(detected_elements, [])
            # enable if uses OpenCv-contrib-python
            # display.display_frames()

            deep.save_to_db() if detected_elements else None
            video_request.put(display.frame_to_stream())
            elements_request.put(json.dumps(detected_elements))

            for i in range(int(1.0 / (time.time() - start_time))):
                stream_queue.get()
            # enable if uses OpenCv-contrib-python
            # if cv.waitKey(1) & 0xFF == ord('q'):
            #     break


def socket_connection():
    server = SocketServerSide(host='127.0.0.1', port=65432)
    server.video_connection()


def api_connection():
    server = SocketServerSide(host='127.0.0.1', port=65431)
    server.establish_connection()


def process():
    p1 = threading.Thread(target=frame_grabber)
    p2 = threading.Thread(target=result)
    p3 = threading.Thread(target=socket_connection)
    p4 = threading.Thread(target=api_connection)
    p1.start()
    p2.start()
    p3.start()
    p4.start()


if __name__ == '__main__':
    process()
