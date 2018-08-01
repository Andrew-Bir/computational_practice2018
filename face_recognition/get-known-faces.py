import face_recognition
import os

face_encodings = []
face_names = []

for file in os.listdir("known_faces"):
    if file.endswith(".jpg"):
        face_names.append((os.path.splitext(file)[0]).replace("_", " "))
        # Load the jpg files into numpy arrays
        image = face_recognition.load_image_file(os.path.join("known_faces", file))
        # --------------------------------------------------------------------------
        # Get the face encodings for each face in each image file:
        # list_of_face_encodings = face_recognition.face_encodings(image)
        # it returns a list of encodings.
        # But since I know each image only has one face, I only care about the first encoding in each image,
        # so I take index 0.
        # --------------------------------------------------------------------------
        face_encoding = face_recognition.face_encodings(image)[0]
        # --------------------------------------------------------------------------
        # Finding the encoding for a face is a bit slow,
        # so you might want to save the results for each image in a database or cache
        # if you need to refer back to it later.
        # --------------------------------------------------------------------------
        face_encodings.append(face_encoding)

with open("arrays.py", mode="wt", encoding="utf-8") as f:
    f.write("# arrays.py\n\n")
    f.write("face_names = [")
    for i in range(len(face_names)-1):
        f.write("\""+face_names[i]+"\", ")
    f.write("\""+face_names[len(face_names)-1]+"\"]\n")
    f.write("\n# it's from get-known-faces.py output\n")
    f.write("known_faces = [")
    for i in range(len(face_encodings)-1):
        f.write("\n\t[")
        for j in range(len(face_encodings[i])-1):
            f.write("\n\t\t"+str(face_encodings[i][j])+",")
        f.write("\n\t\t"+str(face_encodings[i][len(face_encodings[i])-1]))
        f.write("\n\t],")
    f.write("\n\t[")
    for n in range(len(face_encodings[len(face_encodings)-1])-1):
        f.write("\n\t\t"+str(face_encodings[len(face_encodings)-1][n])+",")
    f.write("\n\t\t"+str(face_encodings[len(face_encodings)-1][len(face_encodings[len(face_encodings)-1])-1]))
    f.write("\n\t]\n]\n")
    f.write("\n")
f.close()
