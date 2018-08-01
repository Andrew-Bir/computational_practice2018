# face_identify.py
import face_recognition

from arrays import face_names, known_faces

def identify(test_img):
    # Load the jpg files into numpy arrays
    image = face_recognition.load_image_file(test_img)

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown person"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            name = face_names[matches.index(True)]

        names.append(name)

    #print(names)
    return names

if __name__ == "__main__":
    img = "test_data/test8.jpg"
    identify(img)
