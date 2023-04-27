import cv2
import face_recognition
import numpy as np
import os

class ApprovedFaces:
    def __init__(self):
        self.faces_array = np.zeros(128)
        self.names = np.zeros(1)
        self.frame_resizing = 0.25

    def reset_faces(self):
        self.faces_array = np.zeros(128)
        self.names = np.zeros(1)

    def add_face(self, face, name):  # face is name/path of file
        img = cv2.imread(face)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_encoding = np.array(face_recognition.face_encodings(rgb_img)[0])
        # print(self.faces_array, img_encoding, img_encoding.shape)
        self.faces_array = np.vstack((self.faces_array, img_encoding))
        self.names = np.append(self.names, name)

    def add_encodings_in_dir(self):
        for file in os.listdir():
            if file.endswith('.txt') and not file.endswith('addfaces.txt'):
                self.add_encoding(np.loadtxt(file), file[:-4])

    def add_encoding(self, face_encoding, name):
        self.faces_array = np.vstack((self.faces_array, face_encoding))
        self.names = np.append(self.names, name)

    # Returns True if successful, False is name is not found
    def remove_face(self, name):
        for i in self.names:
            if name == i:
                np.delete(self.names, i)
                np.delete(self.faces_array, i)

    # Check if face is in accepted faces list, returns bool and name if found
    def check_face_path(self, face):
        img = cv2.imread(face)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_encoding = face_recognition.face_encodings(rgb_img)[0]
        idx = 0
        for face in self.faces_array:
            if face_recognition.compare_faces([img_encoding], face)[0]:
                return True, self.names[idx]
            idx += 1
        return False, 'Unknown face'

    # Check if face is in accepted faces list, name if found
    def check_face_array(self, given_face):
        idx = 0
        for face in self.faces_array:
            if face_recognition.compare_faces([given_face], face)[0]:
                return self.names[idx]
            idx += 1
        return 'Unknown face'

    # Helper function for detect_known_faces
    # Returns the name of the approved face that is closest to the given face, with a minimum similarity score
    def check_face_lowest_distance(self, given_face):
        lowest_distance = 0.5
        lowest_face_name = 'Unknown face'
        idx = 0
        for face in self.faces_array:
            #print(face, given_face)
            if type(face) == np.float64:
                break
            face_distance = face_recognition.face_distance([face], given_face)
            if face_distance < lowest_distance:
                lowest_face_name = self.names[idx]
                lowest_distance = face_distance
            idx += 1
        return lowest_face_name

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            name = self.check_face_lowest_distance(face_encoding)
            # name = self.check_face_array(face_encoding)
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names
