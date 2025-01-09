from datetime import datetime
from models.face_detector import FaceDetector
from models.attendance_manager import AttendanceManager
from utils.config import Config
import cv2

class FaceAttendanceSystem:
    def __init__(self):
        self.face_detector = FaceDetector()
        self.attendance_manager = AttendanceManager()
        self.config = Config()

    def register_face(self):
        name = input("Masukkan nama Anda: ")
        print("Sedang mengambil gambar wajah. Mohon tunggu...")
        count = self.face_detector.capture_faces(name, self.config.SAMPLE_COUNT)
        print(f"Berhasil mengambil {count} gambar wajah untuk {name}")

    def train_model(self):
        try:
            self.face_detector.train_model()
            print("Model telah berhasil dilatih dan disimpan.")
        except Exception as e:
            print(f"Gagal melatih model: {str(e)}")

    def scan_faces(self):
        try:
            label_dict = self.face_detector.load_model()
        except FileNotFoundError:
            print("Model belum dilatih. Silakan latih model terlebih dahulu.")
            return

        cam = cv2.VideoCapture(self.config.CAMERA_INDEX)
        attendance_recorded = set()

        while True:
            ret, frame = cam.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face_img = gray[y:y+h, x:x+w]
                label_id, confidence = self.face_detector.face_recognizer.predict(face_img)

                if confidence < self.config.CONFIDENCE_THRESHOLD:
                    name = next(
                        (label for label, id in label_dict.items() if id == label_id),
                        "Unknown"
                    )

                    if name not in attendance_recorded and not self.attendance_manager.check_attendance(name):
                        time = self.attendance_manager.record_attendance(name)
                        attendance_recorded.add(name)
                        print(f"Attendance recorded for {name} at {time}")

                    confidence_text = f"{name} ({100 - int(confidence)}%)"
                else:
                    confidence_text = "Tidak dikenal"

                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, confidence_text, (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            cv2.imshow(self.config.WINDOW_NAME, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

    def view_attendance(self):
        records = self.attendance_manager.get_today_attendance()
        if not records:
            print("Belum ada data absensi untuk hari ini.")
            return

        print(f"\nData Absensi - {datetime.now().strftime('%Y-%m-%d')}")
        print("Nama\t\tWaktu")
        print("-" * 30)
        for name, time in records:
            print(f"{name}\t\t{time}")

    def run(self):
        while True:
            print("\n=== Sistem Absensi Wajah ===")
            print("1. Daftar Wajah")
            print("2. Latih Model")
            print("3. Scan Wajah")
            print("4. Lihat Absensi Hari Ini")
            print("5. Keluar")

            choice = input("Pilih menu (1/2/3/4/5): ")

            actions = {
                "1": self.register_face,
                "2": self.train_model,
                "3": self.scan_faces,
                "4": self.view_attendance,
                "5": lambda: print("Keluar dari program.")
            }

            if choice in actions:
                if choice == "5":
                    actions[choice]()
                    break
                actions[choice]()
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    system = FaceAttendanceSystem()
    system.run()
