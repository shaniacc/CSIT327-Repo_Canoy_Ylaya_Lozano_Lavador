from flask import Flask, render_template, Response,request,flash,redirect,url_for,current_app
from flask_sqlalchemy import SQLAlchemy
import cv2
from face_recognition_api import FaceRecognition
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FileField
from wtforms.validators import DataRequired,Email
from flask_migrate import Migrate
import numpy as np
app = Flask(__name__)
face_recognizer = FaceRecognition()

app.config['SQLALCHEMY_DATABASE_URI']  = 'mysql+pymysql://attendanceadmin:tearoff1attendance@db4free.net/attendancesys'
app.config['SECRET_KEY'] = 'IM2'

db  = SQLAlchemy(app)
migrate = Migrate(app,db)


#database column creation 
class Student(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(50),nullable = False)  
    last_name  = db.Column(db.String(50),nullable = False) 
    roll_number = db.Column(db.String(15), nullable = False )
    faceImage = db.Column(db.LargeBinary, nullable = False)
    def __repr__(self):
        return f'<Student {self.Student_id}>'

    #face_econding value not yet finalized; probably integer or BLOB
class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key = True)
    course_name = db.Column(db.String(50),nullable = False)
    course_code = db.Column(db.String(50),unique = True,nullable = False)
    time_slot = db.Column(db.String(50),nullable = False)
    def __repr__(self):
        return f'<Course  {self.course_id}>'

class Attendance(db.Model):
    attendance_id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'),nullable = False)
    date = db.Column(db.DateTime(), default = datetime.utcnow())
    attendance_time = db.Column(db.String(50),nullable = False) 
    status = db.Column(db.String(50),nullable = False)
    def __repr__(self) :
        return f'<Attendance {self.attendance_id}>'




class CreateStudentAccForm(FlaskForm):
    first_name  = StringField("First Name",validators =[DataRequired()])
    last_name = StringField("Last Name",validators = [DataRequired()])
    roll_no = StringField("Roll Number", validators=[DataRequired()])
    face_img = FileField("Image",validators = [DataRequired()])
def gen():
    cap = cv2.VideoCapture(0)
    with app.app_context():
        while True:
            success, frame = cap.read()
            students = Student.query.all()
            student_encodings = [
                (student.first_name.encode(), student.last_name.encode(), np.frombuffer(student.faceImage, dtype=np.float64)) for student in students
            ]

            # Call face recognition method
            frame, names = face_recognizer.recognize_faces(frame, student_encodings)

            # Encode frame as JPEG image
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n' 







@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addStudent', methods=['GET', 'POST'])
def addStudent():
    form = CreateStudentAccForm()
    if form.validate_on_submit():
        encoded_img = request.files['face_img']
        uploaded_image = cv2.imdecode(np.frombuffer(encoded_img.read(), np.uint8), -1)
        uploaded_encoding = face_recognizer._find_encodings([cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)])[0]
        # Encode the face image as bytes before storing it in the database
        face_image_bytes = np.asarray(uploaded_encoding).tobytes()
        newStudent = Student(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            roll_number=form.roll_no.data,
            faceImage=face_image_bytes  # Store the face image as bytes in the database
        )
        db.session.add(newStudent)
        db.session.commit()
        flash('User added Successfully')
        return redirect(url_for('addStudent'))
    else:
        flash('INVALID INPUT')

    return render_template('addStudent.html', form=form)




@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
