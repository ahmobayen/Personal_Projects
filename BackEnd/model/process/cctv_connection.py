# Libraries
# System Libraries
import os
import platform
import subprocess
import re
from model.widespread.logger import Logger
from model.joint.static_paths import VIDEO_PATH
from model.joint.in_app_parameters import CCTV_CONNECTION


class CheckConnection:
    def __init__(self, input_media):
        """input must be dictionary in format for the given url:
        {protocol}://""{username}:{password}@{ip}:{port}/Streaming/Channels/{sub_channel}/

            'ip': VALUE
            'protocol': VALUE: http or rtsp,
            'username': VALUE
            'password': VALUE,
            'port': VALUE: default port for rtsp is 554,
            'sub_channel': VALUE
        """
        self.status = bool
        self.input_media = {
            'protocol': input_media['protocol'],
            'username': input_media['username'],
            'ip': input_media['ip'],
            'password': input_media['password'],
            'port': input_media['port'],
            'sub_channel': input_media['sub_channel']
            }
        self.url = str
        self.url_for_log = str
        self.logging = Logger('connection')

    def ping(self):
        response = subprocess.run(
            ["ping", self.input_media['ip'], "-n" if platform.system().lower() == "windows" else "-c", "1"],
            stdout=subprocess.PIPE)
        status = True if re.search("time", str(response)) else False
        self.logging.info('Connection accessibility status is:', status)
        return status

    def check_connection(self):
        if self.status:
            self.url = "{protocol}://""{username}:{password}@{ip}:{port}/Streaming/Channels/{sub_channel}/" \
                .format(protocol=self.input_media['protocol'], username=self.input_media['username'],
                        ip=self.input_media['ip'],
                        password=self.input_media['password'], port=self.input_media['port'],
                        sub_channel=self.input_media['sub_channel'])
            self.url_for_log = "{protocol}://""username:********@{ip}:{port}/Streaming/Channels/{sub_channel}/" \
                .format(protocol=self.input_media['protocol'], ip=self.input_media['ip'],
                        port=self.input_media['port'], sub_channel=self.input_media['sub_channel'])
            self.logging.info('CCTV connection connected successfully to:', self.url_for_log)
        else:
            # self.url = os.path.join(VIDEO_PATH, 'parking_lot_1.mp4')
            # self.url = os.path.join(VIDEO_PATH, 'street.MOV')
            self.url = os.path.join(VIDEO_PATH, 'office.mp4')
            self.logging.error('unable to make connection with CCTV. check your connection!')
        return str(self.url)


if __name__ == '__main__':
    connection = CheckConnection(CCTV_CONNECTION)
    connection.check_connection()