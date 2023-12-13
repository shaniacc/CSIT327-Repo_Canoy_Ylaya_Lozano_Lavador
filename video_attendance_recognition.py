
from flask import Flask
from face_recognition_api import FaceRecognition
from models import *;
from face_recognition import face_locations
from datetime import datetime,timedelta
from insertion_procedures import insert_attendance_procedure
import cv2

face_recognizer = FaceRecognition()


def gen(selected_course_id,app):
    cap = cv2.VideoCapture(0)

    with app.app_context():
        while True:
            success, frame = cap.read()
            students = Student.query.all()
            student_encodings = [
                (student.first_name, student.last_name, student.faceImage, student.id) for student in students
            ]

            # Call face recognition method
            frame, names = face_recognizer.recognize_faces(frame, student_encodings)

            if not names:
                cv2.putText(frame, 'No Face Detected', (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                # Get the current time
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Iterate through detected names
                for name, student_id in names:
                    # Check if the student has already been marked for attendance within a time window (e.g., 5 seconds)
                    existing_attendance = Attendance.query.filter_by(student_id=student_id, course_id=selected_course_id).filter(Attendance.date > (datetime.now() - timedelta(seconds=5))).first()

                    if existing_attendance:
                        # If already marked, skip
                        continue
                     # Fetch the course object
                    course = Courses.query.get(selected_course_id)

                    if course and course.start_time <= datetime.now().time() <= course.end_time:
                        # Record attendance as 'Present'
                        status = 'Present'
                    else:
                        # Record attendance as 'Absent'
                        status = 'Absent'
                    # Record attendance
                    insert_attendance_procedure(
                        student_id=student_id,
                        course_id=selected_course_id,
                        date=datetime.now(),
                        attendance_time=current_time,
                        status=status
                    )

                    # Save to the database
                 

            # Encode frame as JPEG image
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes
