import cv2
import os
import numpy as np
import pickle
from datetime import datetime

class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.model_file = "model.yml"
        self.labels_file = "labels.pkl"
        self.dataset_folder = "dataset"

    def ensure_dataset_folder(self):
        if not os.path.exists(self.dataset_folder):
            os.makedirs(self.dataset_folder)

    def capture_faces(self, name, num_samples=20):
        self.ensure_dataset_folder()
        cam = cv2.VideoCapture(0)
        count = 0

        while True:
            ret, frame = cam.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                count += 1
                face_img = gray[y:y+h, x:x+w]
                file_name = f"{self.dataset_folder}/{name}_{count}.jpg"
                cv2.imwrite(file_name, face_img)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            cv2.imshow("Wajah", frame)

            if cv2.waitKey(1) & 0xFF == ord('q') or count >= num_samples:
                break

        cam.release()
        cv2.destroyAllWindows()
        return count

    def train_model(self):
        if not os.path.exists(self.dataset_folder):
            raise FileNotFoundError("Dataset folder not found")

        images = []
        labels = []
        label_dict = {}
        label_id = 0

        for file in os.listdir(self.dataset_folder):
            if file.endswith(".jpg"):
                label = file.split("_")[0]
                if label not in label_dict:
                    label_dict[label] = label_id
                    label_id += 1

                img_path = os.path.join(self.dataset_folder, file)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                images.append(img)
                labels.append(label_dict[label])

        if not images:
            raise ValueError("No images found in dataset")

        self.face_recognizer.train(images, np.array(labels))
        self.face_recognizer.save(self.model_file)

        with open(self.labels_file, "wb") as f:
            pickle.dump(label_dict, f)

    def load_model(self):
        if not all(os.path.exists(f) for f in [self.model_file, self.labels_file]):
            raise FileNotFoundError("Model files not found")

        self.face_recognizer.read(self.model_file)
        with open(self.labels_file, "rb") as f:
            return pickle.load(f)

