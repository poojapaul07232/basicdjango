import face_recognition
import os, pickle

def teachFace(picture, name, facefile = None):
    name_image = face_recognition.load_image_file(picture)
    face_locations = face_recognition.face_locations(name_image, model="cnn")
    faces = face_recognition.face_encodings(name_image,known_face_locations=face_locations,num_jitters=1)
    if len(faces) > 1 :
        return(2,'Too Many Faces !')
    elif len(faces) == 0:
        return(2,'No Face Found !')
    else:
        exists = os.path.isfile(facefile)
        if exists:
            fileobj = open(facefile,'rb')
            facelist = pickle.load(fileobj)
            fileobj.close()
            faces = faces + facelist
        fileobj = open(facefile,'wb')
        pickle.dump(faces,fileobj)
        fileobj.close()
    return(0,'Learnt !')

def findFace(picture, pkl):
    name_image = face_recognition.load_image_file(picture)
    face_locations = face_recognition.face_locations(name_image, model="cnn")
    # face_locations = face_recognition.face_locations(name_image)
    faces = face_recognition.face_encodings(name_image,known_face_locations=face_locations,num_jitters=1)
    # faces = face_recognition.face_encodings(name_image)
    if len(faces) == 0:
        return (2,'No Face Found !')
    fileobj = open(pkl,'rb')
    face_list = pickle.load(fileobj)
    for j in faces:
        result = face_recognition.compare_faces(face_list, j)
        if result:
            return(0,'Matched !')
    return(1,'No Match !')
    