from MySQLdb import IntegrityError
from flask import flash
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from models import db

def insert_student_procedure(first_name, last_name, roll_number, face_image):
    try:
        sql_query = text("CALL insert_student(:first_name, :last_name, :roll_number, :face_image)")
        db.session.execute(sql_query, {"first_name": first_name, "last_name": last_name, "roll_number": roll_number, "face_image": face_image})
        db.session.commit()
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
    finally:
        db.session.close()



def insert_course_procedure(course_name, course_code, start_time, end_time):
    try:
        sql_query = text("CALL insert_course(:course_name, :course_code, :start_time, :end_time)")
        db.session.execute(sql_query, {"course_name": course_name, "course_code": course_code, "start_time": start_time, "end_time": end_time})
        db.session.commit()
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
    finally:
        db.session.close()


def insert_attendance_procedure(student_id , course_id , date , attendance_time ,  status):
    try:
        sql_query = text("CALL insert_attendance(:student_id,  :course_id, :date, :attendance_time, :status)")
        db.session.execute(sql_query,{"student_id":student_id, "course_id":course_id, "date":date, "attendance_time":attendance_time, "status":status})
        db.session.commit()
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
    finally:
        db.session.close()


def update_student_procedure(student_id ,first_name , last_name , roll_number ):
    try:
        sql_query = text("CALL UpdateStudent(:student_id, :first_name, :last_name, :roll_number)")
        db.session.execute(sql_query,{
            "student_id": student_id, 
            "first_name": first_name, 
            "last_name": last_name, 
            "roll_number": roll_number})
        db.session.commit()
    except Exception as e:
        print(f"Error as {e}")
        db.session.rollback()
    finally:
        db.session.close()

def update_course_procedure(course_id, new_course_name, new_course_code, new_start_time, new_end_time):
    try:
        sql_query = text("CALL UpdateCourse(:course_id, :new_course_name, :new_course_code, :new_start_time, :new_end_time)")
        db.session.execute(
            sql_query,
            {
                "course_id": course_id,
                "new_course_name": new_course_name,
                "new_course_code": new_course_code,
                "new_start_time": new_start_time,
                "new_end_time": new_end_time,
            },
        )
        db.session.commit()
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
    finally:
        db.session.close()

