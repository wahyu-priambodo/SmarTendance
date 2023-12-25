from flask_restx import fields

from ..extensions import api

"""
1. class model (DONE)
2. room model  (DONE)
3. student model (ON PROGRESS)
4. lecturer model
5. course model
6. lecturer attendance log model
7. student attendance log model
"""

""" List model. """
class_list_model = api.model("ClassList", {
  "class_id": fields.String,
  "major": fields.String(attribute=lambda x: x.major.value),
  "study_program": fields.String(attribute=lambda x: x.study_program.value)
})

room_list_model = api.model("RoomList", {
  "room_id": fields.String,
  "room_building": fields.String(attribute=lambda x: x.room_building.value),
  "room_description": fields.String
})

admin_list_model = api.model("AdminList", {
  "user_id": fields.String,
  "user_fullname": fields.String,
  "user_email_address": fields.String,
  "user_home_address": fields.String
})

student_list_model = api.model("StudentList", {
  "student_uuid": fields.String,
  "student_nim": fields.String,
  "student_fullname": fields.String,
  "student_class": fields.String,
  "student_email_address": fields.String,
  "student_home_address": fields.String,
  "date_entry": fields.Date,
  "student_courses": fields.Raw
})

lecturer_list_model = api.model("LecturerList", {
  "lecturer_uuid": fields.String,
  "lecturer_nip": fields.String,
  "lecturer_fullname": fields.String,
  "lecturer_major": fields.String,
  "lecturer_email_address": fields.String,
  "lecturer_home_address": fields.String,
  "date_entry": fields.Date,
  "lecturer_courses": fields.Raw
})

course_list_model = api.model("CourseList", {
  "course_id": fields.String,
  "course_name": fields.String,
  "lecturer_nip": fields.String,
  "class_id": fields.String,
  "room_id": fields.String,
  "day": fields.String,
  "time_start": fields.String,
  "time_end": fields.String,
  "course_description": fields.String,
  "list_of_students": fields.Raw
})

lecturer_attendance_logs_model = api.model("LecturerAttendanceLogs", {
  "log_id": fields.Integer,
  "lecturer_nip": fields.String,
  "course_id": fields.String,
  "room_id": fields.String,
  "time_in": fields.String,
  "time_out": fields.String,
  "day": fields.String(attribute=lambda x: x.day.value),
})

student_attendance_logs_model = api.model("StudentAttendanceLogs", {
  "log_id": fields.Integer,
  "student_nim": fields.String,
  "course_id": fields.String,
  "room_id": fields.String,
  "status": fields.String(attribute=lambda x: x.status.value),
  "time_in": fields.String,
  "time_out": fields.String,
  "day": fields.String(attribute=lambda x: x.day.value),
})

""" Input model for create and edit action. """
admin_input_model = api.model("AdminInput", {
  "user_id": fields.String(required=True, description="Admin ID"),
  "user_fullname": fields.String(required=True, description="Admin Fullname"),
  "user_password": fields.String(required=True, description="Admin Password"),
  "user_email_address": fields.String(required=True, description="Admin Email Address"),
  "user_home_address": fields.String(required=False, description="Admin Home Address"),
})

student_input_model = api.model("StudentInput", {
  "student_nim": fields.String(required=True, description="Student NIM"),
  "student_fullname": fields.String(required=True, description="Student Fullname"),
  "student_password": fields.String(required=True, description="Student Password"),
  "student_card_uid": fields.String(required=True, description="Student Card UID"),
  "student_class": fields.String(required=True, description="Student Class"),
  "student_email_address": fields.String(required=True, description="Student Email Address"),
  "student_home_address": fields.String(required=False, description="Student Home Address"),
})

lecturer_input_model = api.model("LecturerInput", {
  "lecturer_nip": fields.String(required=True, description="Lecturer NIP"),
  "lecturer_fullname": fields.String(required=True, description="Lecturer Fullname"),
  "lecturer_password": fields.String(required=True, description="Lecturer Password"),
  "lecturer_card_uid": fields.String(required=True, description="Lecturer Card UID"),
  "lecturer_major": fields.String(required=True, description="Lecturer Major"),
  "lecturer_email_address": fields.String(required=True, description="Lecturer Email Address"),
  "lecturer_home_address": fields.String(required=False, description="Lecturer Home Address"),
})

course_input_model = api.model("CourseInput", {
  "course_id": fields.String(required=True, description="Course ID"),
  "course_name": fields.String(required=True, description="Course Name"),
  "lecturer_nip": fields.String(required=True, description="Lecturer NIP"),
  "class_id": fields.String(required=True, description="Class ID"),
  "room_id": fields.String(required=True, description="Room ID"),
  "day": fields.String(required=True, description="Day"),
  "time_start": fields.String(required=True, description="Time Start"),
  "time_end": fields.String(required=True, description="Time End"),
  "course_description": fields.String(required=False, description="Course Description"),
})