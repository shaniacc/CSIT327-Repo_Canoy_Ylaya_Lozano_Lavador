import cv2
import numpy as np
import face_recognition

class FaceRecognition():
    def __init__(self):
        self.encodeListKnown = []

    def _find_encodings(self, images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList
 
        
    def recognize_faces(self, frame, student_data):
        student_encodings = [np.frombuffer(encoding, dtype=np.float64) for _, _, encoding, _ in student_data]
        student_names = [(None, None) for _ in student_data]  # Placeholder for names since they are not provided

        imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
        names = []

        for encodeFace, FaceLoc in zip(encodeCurFrame, faceCurFrame):
            # Ensure that encodeFace has the correct data type
            encodeFace = encodeFace.astype(np.float64)

            matches = face_recognition.compare_faces(student_encodings, encodeFace)

            if any(matches):
                faceDis = face_recognition.face_distance(student_encodings, encodeFace)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    student_id = student_data[matchIndex][3]
                    name = f"Student {student_id}"  # Use a generic name since actual names are not provided
                    names.append((name, student_id))
                    y1, x2, y2, x1 = FaceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        return frame, names





