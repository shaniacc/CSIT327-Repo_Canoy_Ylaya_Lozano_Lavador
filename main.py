from flask import Flask, render_template, Response,request,flash,redirect,url_for,current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import cv2
from face_recognition_api import FaceRecognition
from face_recognition import face_locations
from datetime import datetime,timedelta
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FileField,TimeField,SelectField
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

    
class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key = True)
    course_name = db.Column(db.String(50),nullable = False)
    course_code = db.Column(db.String(50),unique = True,nullable = False)
    start_time = db.Column(db.Time(), nullable = False)
    end_time = db.Column(db.Time(), nullable = False)
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



#form for creating a student 
class CreateStudentAccForm(FlaskForm):
    first_name  = StringField("First Name",validators =[DataRequired()])
    last_name = StringField("Last Name",validators = [DataRequired()])
    roll_no = StringField("Roll Number", validators=[DataRequired()])
    face_img = FileField("Image",validators = [DataRequired()])
    submit = SubmitField("Submit")
#Fform for creating a course 
class CreateCourseForm(FlaskForm):
    course_name = StringField("Course Name",validators = [DataRequired()])
    course_code = StringField("Course Code",validators = [DataRequired()])
    start_time = TimeField("Start Time",validators = [DataRequired()])
    end_time = TimeField("End Time",validators = [DataRequired()])
    submit = SubmitField("Submit")
class UpdateStudentForm(FlaskForm):
    update_first_name  = StringField("First Name",validators =[DataRequired()])
    update_last_name = StringField("Last Name",validators = [DataRequired()])
    update_roll_no = StringField("Roll Number", validators=[DataRequired()])
    update_face_img = FileField("Image")
    submit = SubmitField("Submit")
class UpdateCourseForm(FlaskForm):
    update_course_name = StringField("Course Name",validators = [DataRequired()])
    update_course_code = StringField("Course Code",validators = [DataRequired()])
    update_start_time = TimeField("Start Time",validators = [DataRequired()])
    update_end_time = TimeField("End Time",validators = [DataRequired()])
    submit = SubmitField("Submit")
class SelectCourseForm(FlaskForm):
    course = SelectField("Select Course", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Submit")

def gen(selected_course_id):
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
                    new_attendance = Attendance(
                        student_id=student_id,
                        course_id=selected_course_id,
                        date=datetime.now(),
                        attendance_time=current_time,
                        status=status
                    )

                    # Save to the database
                    try:
                        db.session.add(new_attendance)
                        db.session.commit()
                    except IntegrityError:
                        # Handle if the attendance record already exists (e.g., due to simultaneous requests)
                        db.session.rollback()

            # Encode frame as JPEG image
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes








@app.route('/addStudent', methods=['GET', 'POST'])
def addStudent():
    form = CreateStudentAccForm()
    if form.validate_on_submit():
        
        checkStudent = Student.query.filter_by(roll_number = form.roll_no.data).first() # This will query out roll_numbers in the databsae 
        if checkStudent is None: # This will check if the student already exist or not   
            encoded_img = request.files['face_img']
            uploaded_image = cv2.imdecode(np.frombuffer(encoded_img.read(), np.uint8), -1)
            faceCheck = face_locations(uploaded_image)
        # Encode the face image as bytes before storing it in the database
            if not faceCheck:
                flash('Invalid Student Image')
                return redirect(url_for('addStudent'))
            uploaded_encoding = face_recognizer._find_encodings([cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)])[0]
            face_image_bytes = np.asarray(uploaded_encoding).tobytes()
            newStudent = Student(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                roll_number=form.roll_no.data,
                faceImage=face_image_bytes  # Store the face image as bytes in the database
            )
            db.session.add(newStudent)
            db.session.commit()
            flash('Student Record Added Successfully')
            return redirect(url_for('addStudent'))
        else:
            flash('Student Record Already Exists')
            return redirect(url_for('addStudent'))

    return render_template('addStudent.html', form=form)

@app.route('/addCourse',methods=['GET', 'POST'])
def addCourse():
    form = CreateCourseForm()
    if form.validate_on_submit():
        newCourse = Courses(
            course_name=form.course_name.data,
            course_code=form.course_code.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data
            
        )
        db.session.add(newCourse)
        db.session.commit()
        flash('Course added Successfully')
        return redirect(url_for('addCourse'))
  

    return render_template('addCourse.html', form=form)

@app.route('/Studentlist',methods=['GET'])
def StudentList():
    students = Student.query.all()
    return render_template('StudentList.html',students=students)


@app.route('/updateStudent/<int:id>', methods=['GET', 'POST'])
def updateStudent(id):
    form = UpdateStudentForm()
    student_to_update = Student.query.get_or_404(id)

    if request.method == 'POST' and form.validate_on_submit():
        update_face_img = request.files.get('update_face_img')  # Use get() method to handle optional file upload

        if update_face_img:  # Check if a new image is provided
            uploaded_image = cv2.imdecode(np.frombuffer(update_face_img.read(), np.uint8), -1)
            faceCheck = face_locations(uploaded_image)

            if not faceCheck:## Check if face image is valid or not
                flash('Invalid Student Image')
                return redirect(url_for('updateStudent', id=id))

            uploaded_encoding = face_recognizer._find_encodings([cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)])[0]
            face_image_bytes = np.asarray(uploaded_encoding).tobytes()
            student_to_update.faceImage = face_image_bytes

        # Update textual information (first name, last name, and roll number)
        student_to_update.first_name = form.update_first_name.data
        student_to_update.last_name = form.update_last_name.data
        student_to_update.roll_number = form.update_roll_no.data

        try:
            db.session.commit()
            flash('Student Record Updated Successfully')
            return redirect(url_for('updateStudent', id=id))
        except:
            flash('Error in updating student record')
            return redirect(url_for('updateStudent', id=id))

    return render_template('updateStudent.html', form=form, student_to_update=student_to_update, id=id)
@app.route('/CourseList',methods=['GET'])
def CourseList():
    courses = Courses.query.all()
    return render_template('CourseList.html',courses=courses)

@app.route('/updateCourse/<int:course_id>', methods=['GET', 'POST'])
def updateCourse(course_id):
    form = UpdateCourseForm() 
    course_to_update = Courses.query.get_or_404(course_id)
    
    if request.method == 'POST' and form.validate_on_submit():
        course_to_update.course_name = form.update_course_name.data
        course_to_update.course_code = form.update_course_code.data
        course_to_update.start_time = form.update_start_time.data
        course_to_update.end_time = form.update_end_time.data
        
        try:
            db.session.commit()
            flash('Course Record Updated Successfully')
            return redirect(url_for('updateCourse', course_id=course_id))
        except Exception as e:
            print(e)
            db.session.rollback()  # Rollback the session to avoid leaving the database in a partially updated state
            flash(f'Error in updating course record: {e}')
            return redirect(url_for('updateCourse', course_id=course_id))
    else:
        print("Form not submitted successfully. Form errors:", form.errors)

    return render_template('updateCourse.html', form=form, course_to_update=course_to_update, course_id=course_id)


@app.route('/deleteStudent/<int:id>',methods=['GET','POST'])
def deleteStudent(id):
    student_to_delete = Student.query.get_or_404(id)
    try:
        db.session.delete(student_to_delete)
        db.session.commit()
        flash('Student Record Deleted Successfully')
        return redirect(url_for('StudentList'))
    except:
        flash('Error in deleting student record')
        return redirect(url_for('StudentList'))
    


@app.route('/deleteCourse/<int:course_id>',methods=['GET','POST'])
def deleteCourse(course_id):
    course_to_delete = Courses.query.get_or_404(course_id)
    try:
        db.session.delete(course_to_delete)
        db.session.commit()
        flash('Course Record Deleted Successfully')
        return redirect(url_for('CourseList'))
    except:
        flash('Error in deleting course record')
        return redirect(url_for('CourseList'))



@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    # Create a form instance
    course_form = SelectCourseForm()

    # Populate course choices in the form
    course_form.course.choices = [(course.course_id, course.course_name) for course in Courses.query.all()]

    # Set default values
    selected_course_id = None

    if request.method == 'POST' and course_form.validate_on_submit():
        # Get the selected course_id from the form
        selected_course_id = course_form.course.data

    # Render the 'index.html' template with the form and selected_course_id
    return render_template('index.html', course_form=course_form, selected_course_id=selected_course_id)

@app.route('/AttendanceList', methods=['GET'])
def AttendanceList():   
    attendance = Attendance.query.all()
    students = Student.query.all()
    return render_template('AttendanceList.html', attendance=attendance, students=students)



@app.route('/')
def index():
    return redirect('attendance')




@app.route('/video_feed/<int:selected_course_id>')
def video_feed(selected_course_id):
    return Response(gen(selected_course_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    app.run(debug=True)
