import socket, pickle
import face_recognition
import sys

sys.path.append("../face_recognition/")
from face_identify import identify

BUFFER_SIZE = 4096

def main():
    HOST = '127.0.0.1'
    PORT = 9999
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    print('Sock name: {}'.format(sock.getsockname()))

    while True:
        conn, addr = sock.accept()
        print('Connected:', addr)
        try:
            test_img = conn.recv(BUFFER_SIZE)
            if not test_img: break
            # Input image
            img = test_img.decode()
            face_names = identify(img)
            data = pickle.dumps(face_names)
            conn.sendall(data)
        finally:
            # Clean up the connection
            print('Close')
            conn.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
