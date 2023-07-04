<<<<<<< HEAD
#!/usr/bin/env python3
import os.path
import pickle
import struct
import socket
import selectors

sel = selectors.DefaultSelector()
messages = [b'Video Request']


def video_receive():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            client_socket.sendall(b'Video Request')

            data = b""
            payload_size = struct.calcsize("Q")
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4 * 1024)  # 4K
                    if not packet:
                        break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += client_socket.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                if frame:
                    yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        except ConnectionError:
            client_socket.close()


def simple_receive():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65431  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_side_socket:
        server_side_socket.connect((HOST, PORT))
        server_side_socket.sendall(b'api Request')
        data = server_side_socket.recv(1024)
        server_side_socket.close()
        return data


if __name__ == '__main__':
    from ast import literal_eval

    data = str(simple_receive().decode('utf-8') )
    python_dict = literal_eval(data)
    print(python_dict)
=======
#!/usr/bin/env python3
import os.path
import pickle
import struct
import socket
import selectors

sel = selectors.DefaultSelector()
messages = [b'Video Request']


def video_receive():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            client_socket.sendall(b'Video Request')

            data = b""
            payload_size = struct.calcsize("Q")
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4 * 1024)  # 4K
                    if not packet:
                        break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += client_socket.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                if frame:
                    yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        except ConnectionError:
            client_socket.close()


def simple_receive():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65431  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_side_socket:
        server_side_socket.connect((HOST, PORT))
        server_side_socket.sendall(b'api Request')
        data = server_side_socket.recv(1024)
        server_side_socket.close()
        return data


if __name__ == '__main__':
    from ast import literal_eval

    data = str(simple_receive().decode('utf-8') )
    python_dict = literal_eval(data)
    print(python_dict)
>>>>>>> 270786ff41f19b6230c41b27351db543564b1c60
