from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TimeField, SelectField, SubmitField
from wtforms.validators import DataRequired

# Form for creating a student
class CreateStudentAccForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    roll_no = StringField("Roll Number", validators=[DataRequired()])
    face_img = FileField("Image", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Form for creating a course
class CreateCourseForm(FlaskForm):
    course_name = StringField("Course Name", validators=[DataRequired()])
    course_code = StringField("Course Code", validators=[DataRequired()])
    start_time = TimeField("Start Time", validators=[DataRequired()])
    end_time = TimeField("End Time", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Form for updating a student
class UpdateStudentForm(FlaskForm):
    update_first_name = StringField("First Name", validators=[DataRequired()])
    update_last_name = StringField("Last Name", validators=[DataRequired()])
    update_roll_no = StringField("Roll Number", validators=[DataRequired()])
    update_face_img = FileField("Image")
    submit = SubmitField("Submit")

# Form for updating a course
class UpdateCourseForm(FlaskForm):
    update_course_name = StringField("Course Name", validators=[DataRequired()])
    update_course_code = StringField("Course Code", validators=[DataRequired()])
    update_start_time = TimeField("Start Time", validators=[DataRequired()])
    update_end_time = TimeField("End Time", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Form for selecting a course
class SelectCourseForm(FlaskForm):
    course = SelectField("Select Course",  validators=[DataRequired()])
    submit = SubmitField("Submit")
