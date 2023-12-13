
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(50),nullable = False)  
    last_name  = db.Column(db.String(50),nullable = False) 
    roll_number = db.Column(db.String(15), nullable = False )
    faceImage = db.Column(db.LargeBinary, nullable = False)
    last_updated = db.Column(db.DateTime(), nullable = True)
    def __repr__(self):
        return f'<Student {self.Student_id}>'

    
class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key = True)
    course_name = db.Column(db.String(50),nullable = False)
    course_code = db.Column(db.String(50),nullable = False)
    start_time = db.Column(db.Time(), nullable = False)
    end_time = db.Column(db.Time(), nullable = False)
    last_updated = db.Column(db.DateTime(), nullable = True)
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
