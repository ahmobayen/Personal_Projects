#!/usr/bin/env python3
import json

from model.widespread.logger import Logger
from model.widespread.db_connection import SqlDatabaseConnection
import pickle
import struct
import socket
import selectors
import queue

video_request = queue.Queue()
elements_request = queue.Queue()


class SocketServerSide:
    def __init__(self, host, port):
        self.__selector = selectors.DefaultSelector()
        self.logging = Logger('socket_transfer')

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()

        self.logging.info('Server is listening to:', host, port)

    def video_connection(self):
        """prepare a port and stream video to client."""
        while True:
            try:
                client_socket, ip_address = self.server_socket.accept()
                with client_socket:
                    self.logging.info("Connected by", ip_address)
                    while True:
                        ret_frame = video_request.get()
                        frame_to_pickle = pickle.dumps(ret_frame)
                        message = struct.pack("Q", len(frame_to_pickle)) + frame_to_pickle
                        client_socket.sendall(message)
            except ConnectionError:
                self.logging.error(ConnectionError)
                client_socket.close()

    def establish_connection(self):
        """default socket to send data to client"""

        while True:
            client_connection, client_address = self.server_socket.accept()
            with client_connection:
                self.logging.info("Connected by", client_address)
                data = client_connection.recv(1024)
                if data == b'api Request':
                    db_select = SqlDatabaseConnection()
                    db_select.executive_query('select * from passage order by time desc limit 10')
                    result_list = [{'id': i, 'name': item[1], 'direction': item[2],
                                    'time': str(item[3])}for i, item in enumerate(db_select.get_result())]
                    client_connection.sendall(json.dumps(result_list).encode('utf-8'))
                else:
                    break


if __name__ == '__main__':
    server = SocketServerSide('127.0.0.1', 65432)
    server.establish_connection()

