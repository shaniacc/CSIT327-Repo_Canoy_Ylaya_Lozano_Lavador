DELIMITER //

CREATE PROCEDURE insert_attendance_procedure(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_date DATETIME,
    IN p_attendance_time VARCHAR(50),
    IN p_status VARCHAR(50)
)
BEGIN
    INSERT INTO attendance (student_id, course_id, date, attendance_time, status)
    VALUES (p_student_id, p_course_id, p_date, p_attendance_time, p_status);
END//

DELIMITER ;


DELIMITER //

CREATE PROCEDURE insert_course_procedure(
    IN p_course_name VARCHAR(50),
    IN p_course_code VARCHAR(50),
    IN p_start_time TIME,
    IN p_end_time TIME
)
BEGIN
    INSERT INTO courses (course_name, course_code, start_time, end_time)
    VALUES (p_course_name, p_course_code, p_start_time, p_end_time);
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE insert_student_procedure(
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_roll_number VARCHAR(15),
    IN p_face_image BLOB
)
BEGIN
    INSERT INTO student (first_name, last_name, roll_number, faceImage)
    VALUES (p_first_name, p_last_name, p_roll_number, p_face_image);
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE update_course_procedure(
    IN p_course_id INT,
    IN p_new_course_name VARCHAR(50),
    IN p_new_course_code VARCHAR(50),
    IN p_new_start_time TIME,
    IN p_new_end_time TIME
)
BEGIN
    UPDATE courses
    SET
        course_name = p_new_course_name,
        course_code = p_new_course_code,
        start_time = p_new_start_time,
        end_time = p_new_end_time
    WHERE course_id = p_course_id;
END//

DELIMITER ;
DELIMITER //

CREATE PROCEDURE update_student_procedure(
    IN p_student_id INT,
    IN p_new_first_name VARCHAR(50),
    IN p_new_last_name VARCHAR(50),
    IN p_new_roll_number VARCHAR(15)
)
BEGIN
    UPDATE student 
    SET first_name = p_new_first_name, 
        last_name = p_new_last_name, 
        roll_number = p_new_roll_number
    WHERE id = p_student_id;
END//

DELIMITER ;

select `attendancesys`.`student`.`first_name` AS `first_name`,`attendancesys`.`student`.`last_name` AS `last_name`,`attendancesys`.`courses`.`course_name` AS `course_name`,`attendancesys`.`attendance`.`date` AS `date`,`attendancesys`.`attendance`.`status` AS `status` 
from ((`attendancesys`.`student` join `attendancesys`.`attendance` on((`attendancesys`.`student`.`id` = `attendancesys`.`attendance`.`student_id`))) join `attendancesys`.`courses` on((`attendancesys`.`attendance`.`course_id` = `attendancesys`.`courses`.`course_id`)))


DELIMITER //

CREATE TRIGGER update_student_timestamp
BEFORE UPDATE ON student
FOR EACH ROW
SET NEW.last_updated = CONVERT_TZ(NOW(), 'UTC', '+8:00');

//

DELIMITER ;
DELIMITER //

CREATE TRIGGER update_course_timestamp
BEFORE UPDATE ON courses
FOR EACH ROW
SET NEW.last_updated = CONVERT_TZ(NOW(), 'UTC', '+8:00');

//

DELIMITER ;


