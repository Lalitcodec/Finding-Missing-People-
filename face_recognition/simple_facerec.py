import face_recognition
import cv2
import os
import glob
import numpy as np

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_resizing = 0.25  # Resize frame for faster processing

    def load_encoding_images(self, images_path):
        """
        Load and encode images from the given path.
        """
        images_path = glob.glob(os.path.join(images_path, "*.*"))
        print("{} encoding images found.".format(len(images_path)))

        for img_path in images_path:
            img = cv2.imread(img_path)
            if img is None:
                print(f"Warning: Unable to read {img_path}")
                continue  # Skip unreadable images

            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            basename = os.path.basename(img_path)
            filename, _ = os.path.splitext(basename)

            # Get encoding
            img_encodings = face_recognition.face_encodings(rgb_img)
            if len(img_encodings) > 0:
                self.known_face_encodings.append(img_encodings[0])
                self.known_face_names.append(filename)
            else:
                print(f"Warning: No face detected in {img_path}")

        print("Encoding images loaded.")

    def detect_known_faces(self, frame):
        """
        Detect known faces in a given frame.
        """
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect face locations and encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            if not self.known_face_encodings:
                face_names.append("Unknown")
                continue  # Skip matching if no known encodings

            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

            name = "Unknown"
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:  # Ensure the match is True
                    name = self.known_face_names[best_match_index]

            face_names.append(name)

        # Convert coordinates to original frame size
        face_locations = (np.array(face_locations) / self.frame_resizing).astype(int)
        return face_locations, face_names
