import socket
from PIL import Image
import cv2 as cv, numpy
import time, datetime, os

import face_recognition
import sys

sys.path.append("../face_recognition/")
from face_identify import identify

def clf(fname):
    # Model parameters
    dir_path = "data/haarcascades" # modify this for your environment
    model_path = dir_path + "/" + fname
    # Create the classifier
    return cv2.CascadeClassifier(model_path)

def main():
    HOST = '127.0.0.1'
    PORT = 9999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        try:
            fname = conn.recv(2048)
            if not fname: break
            # Input image
            image_path = fname.decode()
            msg = identify(image_path)
            # run window
            img = cv.imread(image_path)
            cv.imshow(msg,img)
            cv.waitKey(3000)
            cv.destroyAllWindows()

            bytes = str.encode(msg)
            conn.send(bytes)
        finally:
            # Clean up the connection
            conn.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
