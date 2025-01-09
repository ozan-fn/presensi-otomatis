from datetime import datetime
import os

class AttendanceManager:
    def __init__(self):
        self.attendance_dir = "attendance"
        self.ensure_attendance_folder()

    def ensure_attendance_folder(self):
        if not os.path.exists(self.attendance_dir):
            os.makedirs(self.attendance_dir)

    def get_attendance_file(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.attendance_dir, f"attendance_{today}.txt")

    def check_attendance(self, name):
        attendance_file = self.get_attendance_file()
        if os.path.exists(attendance_file):
            with open(attendance_file, "r") as f:
                return any(name in line for line in f)
        return False

    def record_attendance(self, name):
        attendance_file = self.get_attendance_file()
        current_time = datetime.now().strftime("%H:%M:%S")
        
        with open(attendance_file, "a") as f:
            f.write(f"{name},{current_time}\n")
        
        return current_time

    def get_today_attendance(self):
        attendance_file = self.get_attendance_file()
        if not os.path.exists(attendance_file):
            return []
        
        records = []
        with open(attendance_file, "r") as f:
            for line in f:
                name, time = line.strip().split(",")
                records.append((name, time))
        return records

