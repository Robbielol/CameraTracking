import face_recognition
import face_recognition as fr
import numpy as np
import os, cv2


class Faces:

    def get_encoded_faces(self):
        """
            looks through the faces folder and encodes all
            the faces

            :return: dict of (name, image encoded)
            """
        encoded = {}

        for dirpath, dnames, fnames in os.walk("./faces"):
            for f in fnames:
                if f.endswith(".jpg") or f.endswith(".png"):
                    face = fr.load_image_file("faces/" + f)
                    encoding = fr.face_encodings(face)[0]
                    encoded[f.split(".")[0]] = encoding

        return encoded

    def unknown_image_encoded(self, img):
        """
        encode a face given the file name
        """
        face = fr.load_image_file("faces/" + img)
        encoding = fr.face_encodings(face)[0]

        return encoding

    def classify_face(self, frame):
        """
        will find all of the faces in a given image and label
        them if it knows what they are

        :param frame: The frame is used as the img.
        :param im: str of file path
        :return: list of face names
        """
        faces = self.get_encoded_faces()
        faces_encoded = list(faces.values())
        known_face_names = list(faces.keys())

        # img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
        # img = img[:,:,::-1]
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=5)
        unknown_face_encodings = face_recognition.face_encodings(frame, faces)

        face_names = []
        for face_encoding in unknown_face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(faces_encoded, face_encoding)
            name = "Unknown"

            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            for (x, y, w, h), name in zip(faces, face_names):
                # Draw a box around the face
                cv2.rectangle(frame, (x + w, y + h), (x, y), (0, 0, 255), 3)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (x + w, y + h + 25), (x, y + h), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (x, y+h+20), font, 1.0, (255, 255, 255), 2)

        return frame
        # Display the resulting image
        """
        while True:

            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return face_names"""
