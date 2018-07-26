import face_recognition

# Load the jpg files into numpy arrays
reynolds_image = face_recognition.load_image_file("known_faces/Ryan_Reynolds.jpg")
stone_image = face_recognition.load_image_file("known_faces/Emma_Stone.jpg")
dobrev_image = face_recognition.load_image_file("known_faces/Nina_Dobrev.jpg")

try:
    # --------------------------------------------------------------------------
    # Get the face encodings for each face in each image file:
    # list_of_face_encodings = face_recognition.face_encodings(image)
    # it returns a list of encodings.
    # But since I know each image only has one face, I only care about the first encoding in each image,
    # so I take index 0.
    # --------------------------------------------------------------------------
    reynolds_face_encoding = face_recognition.face_encodings(reynolds_image)[0]
    stone_face_encoding = face_recognition.face_encodings(stone_image)[0]
    dobrev_face_encoding = face_recognition.face_encodings(dobrev_image)[0]
    # --------------------------------------------------------------------------
    # Finding the encoding for a face is a bit slow,
    # so you might want to save the results for each image in a database or cache
    # if you need to refer back to it later.
    # --------------------------------------------------------------------------
except IndexError:
    print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    quit()

a = [
    reynolds_face_encoding,
    stone_face_encoding,
    dobrev_face_encoding
]

for row in a:
    print('[')
    for elem in row:
        print("{}, ".format(elem))
    print('],')
