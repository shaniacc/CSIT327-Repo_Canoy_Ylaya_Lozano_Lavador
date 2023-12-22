from flask import Flask, render_template, Response, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import text
import cv2
from face_recognition_api import FaceRecognition
from face_recognition import face_locations
from flask_migrate import Migrate
import numpy as np
from forms import *
from video_attendance_recognition import gen
from models import Student, Courses, Attendance,db
from insertion_procedures import insert_student_procedure,insert_course_procedure,update_student_procedure,update_course_procedure
app = Flask(__name__)
face_recognizer = FaceRecognition()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://attendanceadmin:tearoff1attendance@db4free.net/attendancesys'
app.config['SECRET_KEY'] = 'IM2'

db.init_app(app)
migrate = Migrate(app, db)







@app.route('/addStudent', methods=['GET', 'POST'])
def addStudent():
    form = CreateStudentAccForm()
    if form.validate_on_submit():
        
        checkStudent = Student.query.filter_by(roll_number = form.roll_no.data).first() # * This will query out roll_numbers in the databsae 
        if checkStudent is None: # * This will check if the student already exist or not   
            encoded_img = request.files['face_img']
            uploaded_image = cv2.imdecode(np.frombuffer(encoded_img.read(), np.uint8), -1)
            faceCheck = face_locations(uploaded_image)
        # * Encode the face image as bytes before storing it in the database
            if not faceCheck:
                flash('Invalid Student Image')
                return redirect(url_for('addStudent'))
            uploaded_encoding = face_recognizer._find_encodings([cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)])[0]
            face_image_bytes = np.asarray(uploaded_encoding).tobytes()
            insert_student_procedure(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                roll_number=form.roll_no.data,
                face_image=face_image_bytes
            )
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
        insert_course_procedure(
            course_name=form.course_name.data,
            course_code=form.course_code.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data
        )
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
        update_face_img = request.files.get('update_face_img')  # * Use get() method to handle optional file upload

        if update_face_img:  #* Check if a new image is provided
            uploaded_image = cv2.imdecode(np.frombuffer(update_face_img.read(), np.uint8), -1)
            faceCheck = face_locations(uploaded_image)

            if not faceCheck:# * Check if face image is valid or not
                flash('Invalid Student Image')
                return redirect(url_for('updateStudent', id=id))

            uploaded_encoding = face_recognizer._find_encodings([cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)])[0]
            face_image_bytes = np.asarray(uploaded_encoding).tobytes()
            student_to_update.faceImage = face_image_bytes

        #* Update textual information (first name, last name, and roll number) using stored procedure
        update_student_procedure(id, form.update_first_name.data, form.update_last_name.data, form.update_roll_no.data)

        try:
            if update_face_img:
                db.session.commit()  # This is only necessary if you're updating the faceImage field
            flash('Student Record Updated Successfully')
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
        try:
            update_course_procedure(
                course_id,
                form.update_course_name.data,
                form.update_course_code.data,
                form.update_start_time.data,
                form.update_end_time.data
            )

            flash('Course Record Updated Successfully')
            return redirect(url_for('updateCourse', course_id=course_id))
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            flash(f'Error in updating course record: {e}')
            return redirect(url_for('updateCourse', course_id=course_id))
    
    return render_template('updateCourse.html', form=form, course_to_update=course_to_update, course_id=course_id)




@app.route('/deleteStudent/<int:id>', methods=['GET', 'POST'])
def deleteStudent(id):
    student_to_delete = Student.query.get_or_404(id)
    try:
        Attendance.query.filter_by(student_id=id).delete()
        db.session.delete(student_to_delete)
        db.session.commit()
        flash('Student Record Deleted Successfully')
        return redirect(url_for('StudentList'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error in deleting student record: {e}')
        return redirect(url_for('StudentList'))
    


@app.route('/deleteCourse/<int:course_id>',methods=['GET','POST'])
def deleteCourse(course_id):
    course_to_delete = Courses.query.get_or_404(course_id)
    try:
        db.session.delete(course_to_delete)
        db.session.commit()
        flash('Course Record Deleted Successfully')
        return redirect(url_for('CourseList'))
    except Exception as e:
        flash('Error in deleting course record')
        return redirect(url_for('CourseList'))



@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    # Create a form instance
    course_form = SelectCourseForm()

    # Populate course choices in the form
    course_form.course.choices = [(str(course.course_id), course.course_name) for course in Courses.query.all()]
    course_form.course.choices.insert(0, ('', '--Select Course--'))
    # Set default values
    selected_course_id = None

    if request.method == 'POST' and course_form.validate_on_submit():
        # Get the selected course_id from the form
        selected_course_id = int(course_form.course.data)  # Convert the selected option to an integer

        # Get the selected course from the database
        selected_course = Courses.query.get_or_404(selected_course_id)

        # Update the selected course using the stored procedure
        update_course_procedure(selected_course_id, selected_course.course_name, selected_course.course_code, selected_course.start_time, selected_course.end_time)

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
    return Response(gen(selected_course_id,app),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    app.run(debug=True)

