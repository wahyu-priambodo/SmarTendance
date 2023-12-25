from flask_restx import Namespace, Resource, abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
import uuid
import pytz
import html

from .models import *
from .api_models import *
from ..decorators import admin_role

ns = Namespace(name='SmarTendanceAPI', path='/', ordered=True, description='SmarTendance REST API v1')
LOCAL_TZ = 'Asia/Jakarta' # change this to your local timezone
DAYS_IN_A_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


""" GET & POST all data """

@ns.route('/administrators')
class AdminListAPI(Resource):
  # method_decorators = [admin_role(), jwt_required()]
  
  @ns.marshal_list_with(admin_list_model)
  def get(self):
    return UserTable.query.filter_by(user_role="Admin").all(), 200

  @ns.expect(admin_input_model)
  def post(self):
    data = ns.payload
    
    user_id = html.escape(data["user_id"])
    user_fullname = html.escape(data["user_fullname"])
    user_password = data["user_password"]
    user_email_address = html.escape(data["user_email_address"])
    user_home_address = html.escape(data["user_home_address"])
    
    # check if user_id already exists
    if UserTable.query.filter_by(user_id=user_id).scalar():
      return abort(400, message="User ID already exists.")
    
    # validate email address
    try:
      validate_email(user_email_address)
    except EmailNotValidError as e:
      return abort(400, message=str(e))
    
    # add new admin to user_tbl
    new_admin = UserTable (
      user_id = user_id,
      user_fullname = user_fullname,
      user_password_hash = generate_password_hash(user_password, method='pbkdf2:sha256'),
      user_role = "Admin",
      user_email_address = user_email_address,
      user_home_address = user_home_address
    )
    
    db.session.add(new_admin)
    db.session.commit()
    
    return {"msg": "Admin added successfully."}, 201


@ns.route('/administrators/classes')
class ClassListAPI(Resource):
  # method_decorators = [admin_role(), jwt_required()]
  
  @ns.marshal_list_with(class_list_model)
  def get(self):
    return ClassTable.query.all(), 200


@ns.route('/administrators/rooms')
class RoomListAPI(Resource):
  # method_decorators = [admin_role(), jwt_required()]
  
  @ns.marshal_list_with(room_list_model)
  def get(self):
    return RoomTable.query.all(), 200


@ns.route('/students')
class StudentListAPI(Resource):
  # method_decorators = [admin_role(), jwt_required()]
  
  @ns.marshal_with(student_list_model)
  def get(self):
    query = db.session.query(StudentTable, ClassTable, UserTable, CourseTable) \
            .join(ClassTable, StudentTable.student_class == ClassTable.class_id) \
            .join(UserTable, UserTable.user_id == StudentTable.student_nim) \
            .outerjoin(CourseTable, CourseTable.class_id == ClassTable.class_id) \
            .add_columns(
              StudentTable.student_uuid,
              StudentTable.student_nim,
              StudentTable.student_class,
              UserTable.user_fullname,
              UserTable.user_email_address,
              UserTable.user_home_address,
              StudentTable.date_entry,
              CourseTable.course_id,
              CourseTable.course_name,
              CourseTable.day,
              CourseTable.time_start,
              CourseTable.time_end
            ) \
            .all()

    results = {}
    for data in query:
      student_uuid = data.student_uuid
      
      if student_uuid not in results:
        results[student_uuid] = {
          "student_uuid": student_uuid,
          "student_nim": data.student_nim,
          "student_fullname": data.user_fullname,
          "student_class": data.student_class,
          "student_email_address": data.user_email_address,
          "student_home_address": data.user_home_address,
          "date_entry": data.date_entry,
          "student_courses": []
        }
      
      if data.course_id:
        course_info = {
          "course_id": data.course_id,
          "course_name": data.course_name,
          "day": data.day.value,
          "time_start": str(data.time_start),
          "time_end": str(data.time_end)
        }
        results[student_uuid]["student_courses"].append(course_info)

    return list(results.values()), 200
  
  @ns.expect(student_input_model)
  def post(self):
    data = ns.payload
    
    student_uuid = str(uuid.uuid4())
    student_nim = html.escape(data["student_nim"])
    student_fullname = html.escape(data["student_fullname"])
    student_password = data["student_password"]
    student_card_uid = data["student_card_uid"]
    student_class = html.escape(data["student_class"])
    student_email_address = html.escape(data["student_email_address"])
    student_home_address = html.escape(data["student_home_address"])
    date_entry = datetime.now(pytz.timezone(LOCAL_TZ)).date()
    
    # check if student_nim exists
    if StudentTable.query.filter_by(student_nim=student_nim).scalar():
      return abort(400, message="Student NIM already exists.") # Bad request
    
    # check if student_class exists
    if not ClassTable.query.filter_by(class_id=student_class).scalar():
      return abort(404, message="Class not found.") # Class not found
    
    # validate email address
    try:
      validate_email(student_email_address)
    except EmailNotValidError as e:
      return abort(400, message=str(e)) # Bad request
    
    # add to user_tbl first
    new_user = UserTable(
      user_id=student_nim,
      user_fullname=student_fullname,
      user_password_hash=generate_password_hash(student_password, method='pbkdf2:sha256'),
      user_rfid_hash=generate_password_hash(student_card_uid, method='pbkdf2:sha256'),
      user_role="Student",
      user_email_address=student_email_address,
      user_home_address=student_home_address,
    )
    db.session.add(new_user)
    db.session.commit()
    
    # then, add to student_tbl
    new_student = StudentTable(
      student_uuid=student_uuid,
      student_nim=student_nim, # foreign key to UserTable
      student_class=student_class, # foreign key to ClassTable
      date_entry=date_entry
    )
    db.session.add(new_student)
    db.session.commit()
    
    return {"msg": "Student added successfully."}, 201


@ns.route('/lecturers')
class LecturerListAPI(Resource):
  # method_decorators = [admin_role(), jwt_required()]
  
  @ns.marshal_with(lecturer_list_model)
  def get(self):
    query = db.session.query(LecturerTable, UserTable, CourseTable) \
            .join(UserTable, UserTable.user_id == LecturerTable.lecturer_nip) \
            .outerjoin(CourseTable, CourseTable.lecturer_nip == LecturerTable.lecturer_nip) \
            .add_columns(
              LecturerTable.lecturer_uuid,
              LecturerTable.lecturer_nip,
              UserTable.user_fullname,
              LecturerTable.lecturer_major,
              UserTable.user_email_address,
              UserTable.user_home_address,
              LecturerTable.date_entry,
              CourseTable.course_id,
              CourseTable.course_name,
              CourseTable.day,
              CourseTable.time_start,
              CourseTable.time_end
            ) \
            .all()

    results = {}
    for data in query:
      lecturer_uuid = data.lecturer_uuid

      if lecturer_uuid not in results:
        results[lecturer_uuid] = {
          "lecturer_uuid": data.lecturer_uuid,
          "lecturer_nip": data.lecturer_nip,
          "lecturer_fullname": data.user_fullname,
          "lecturer_major": data.lecturer_major.value,
          "lecturer_email_address": data.user_email_address,
          "lecturer_home_address": data.user_home_address,
          "date_entry": data.date_entry,
          "lecturer_courses": []
        }

      if data.course_id:
        course_info = {
          "course_id": data.course_id,
          "course_name": data.course_name,
          "day": data.day.value,
          "time_start": str(data.time_start),
          "time_end": str(data.time_end)
        }
        results[lecturer_uuid]["lecturer_courses"].append(course_info)
    
    return list(results.values()), 200

  @ns.expect(lecturer_input_model)
  def post(self):
    data = ns.payload
    
    lecturer_uuid = str(uuid.uuid4())
    lecturer_nip = html.escape(data["lecturer_nip"])
    lecturer_fullname = html.escape(data["lecturer_fullname"])
    lecturer_password = data["lecturer_password"]
    lecturer_card_uid = data["lecturer_card_uid"]
    lecturer_major = html.escape(data["lecturer_major"])
    lecturer_email_address = html.escape(data["lecturer_email_address"])
    lecturer_home_address = html.escape(data["lecturer_home_address"])
    date_entry = datetime.now(pytz.timezone(LOCAL_TZ)).date()
    
    # check if lecturer_nip exists
    if LecturerTable.query.filter_by(lecturer_nip=lecturer_nip).scalar():
      return abort(400, message="Lecturer NIP already exists.") # Bad request
    
    # check if lecturer_major exists
    if not ClassTable.query.filter_by(major=lecturer_major).first():
      return abort(404, message="Major not found.") # Major not found
    
    # validate email address
    try:
      validate_email(lecturer_email_address)
    except EmailNotValidError as e:
      return abort(400, message=str(e)) # Bad request
    
    # add to user_tbl first
    new_user = UserTable(
      user_id=lecturer_nip,
      user_fullname=lecturer_fullname,
      user_password_hash=generate_password_hash(lecturer_password, method='pbkdf2:sha256'),
      user_rfid_hash=generate_password_hash(lecturer_card_uid, method='pbkdf2:sha256'),
      user_role="Lecturer",
      user_email_address=lecturer_email_address,
      user_home_address=lecturer_home_address
    )
    db.session.add(new_user)
    db.session.commit()
    
    # then, add to lecturer_tbl
    new_lecturer = LecturerTable(
      lecturer_uuid=lecturer_uuid,
      lecturer_nip=lecturer_nip, # foreign key to UserTable
      lecturer_major=lecturer_major,
      date_entry=date_entry
    )
    db.session.add(new_lecturer)
    db.session.commit()
    
    return {"msg": "Lecturer added successfully."}, 201


@ns.route('/administrators/courses')
class CourseListAPI(Resource):
  # method_decorators = [admin_role(), jwt_required()]
  
  @ns.marshal_with(course_list_model)
  def get(self):
    query = db.session.query(CourseTable, ClassTable, UserTable, StudentTable) \
            .join(ClassTable, ClassTable.class_id == CourseTable.class_id) \
            .outerjoin(StudentTable, StudentTable.student_class == ClassTable.class_id) \
            .outerjoin(UserTable, UserTable.user_id == StudentTable.student_nim) \
            .add_columns(
              CourseTable.course_id,
              CourseTable.course_name,
              CourseTable.lecturer_nip,
              CourseTable.class_id,
              CourseTable.room_id,
              CourseTable.day,
              CourseTable.time_start,
              CourseTable.time_end,
              CourseTable.course_description,
              StudentTable.student_uuid,
              StudentTable.student_nim,
              UserTable.user_fullname,
              UserTable.user_email_address,
            ) \
            .all()

    results = {}
    for data in query:
      course_id = data.course_id

      if course_id not in results:
        results[course_id] = {
          "course_id": data.course_id,
          "course_name": data.course_name,
          "lecturer_nip": data.lecturer_nip,
          "class_id": data.class_id,
          "room_id": data.room_id,
          "day": data.day.value,
          "time_start": str(data.time_start),
          "time_end": str(data.time_end),
          "course_description": data.course_description,
          "list_of_students": []
        }

      if data.student_uuid:  # Pastikan ada mahasiswa yang terdaftar
        student_info = {
          "student_uuid": data.student_uuid,
          "student_nim": data.student_nim,
          "student_fullname": data.user_fullname,
          "student_email_address": data.user_email_address,
        }
        results[course_id]["list_of_students"].append(student_info)

    return list(results.values()), 200
  
  @ns.expect(course_input_model)
  def post(self):
    data = ns.payload
    
    course_id = html.escape(data["course_id"])
    course_name = html.escape(data["course_name"])
    lecturer_nip = html.escape(data["lecturer_nip"])
    class_id = html.escape(data["class_id"])
    room_id = html.escape(data["room_id"])
    day = html.escape(data["day"].capitalize())
    time_start = html.escape(data["time_start"])
    time_end = html.escape(data["time_end"])
    course_description = html.escape(data["course_description"])
    
    # check if course id exists
    if CourseTable.query.filter_by(course_id=course_id).scalar():
      return abort(400, message="Course ID already exists.")
    
    # check if lecturer_nip exists
    if not LecturerTable.query.filter_by(lecturer_nip=lecturer_nip).scalar():
      return abort(404, message="Lecturer NIP not found.")
    
    # check if class_id exists
    if not ClassTable.query.filter_by(class_id=class_id).scalar():
      return abort(404, message="Class not found.")
    
    # check if room_id exists
    if not RoomTable.query.filter_by(room_id=room_id).scalar():
      return abort(404, message="Room not found.")
    
    # check if day is valid
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    if day not in DAYS_IN_A_WEEK:
      return abort(400, message="Day is not valid.")
    
    # check if time_start and time_end is valid
    try:
      converted_time_start = datetime.strptime(time_start, "%H:%M:%S").time()
      converted_time_end = datetime.strptime(time_end, "%H:%M:%S").time()
    except ValueError as e:
      return abort(400, message=str(e))
    
    # add to course_tbl
    new_course = CourseTable(
      course_id = course_id,
      course_name = course_name,
      lecturer_nip = lecturer_nip,
      class_id = class_id,
      room_id = room_id,
      day = day,
      time_start = str(converted_time_start),
      time_end = str(converted_time_end),
      course_description = course_description
    )
    
    db.session.add(new_course)
    db.session.commit()
    
    return {"msg": "Course added successfully."}, 201


@ns.route('/lecturers/attendance_logs')
class LecturerAttendanceLogsAPI(Resource):
  @ns.marshal_list_with(lecturer_attendance_logs_model)
  def get(self):
    return LecturerAttendanceLogTable.query.all(), 200


@ns.route('/students/attendance_logs')
class StudentAttendanceLogsAPI(Resource):
  @ns.marshal_list_with(student_attendance_logs_model)
  def get(self):
    return StudentAttendanceLogTable.query.all(), 200


""" GET / PUT / DELETE spesific data """
@ns.route('/administrators/<string:user_id>')
class AdminAPI(Resource):
  @ns.marshal_with(admin_list_model)
  def get(self, user_id):
    admin = UserTable.query.filter_by(user_id=user_id, user_role='Admin').scalar()
    
    # check if user_id exists
    if not admin:
      return abort(404, message="User ID not found.")
    
    return admin, 200
  
  @ns.expect(admin_input_model)
  def put(self, user_id):
    data = ns.payload
    
    new_user_id = html.escape(data["user_id"])
    new_user_fullname = html.escape(data["user_fullname"])
    new_user_password = data["user_password"]
    new_user_email_address = html.escape(data["user_email_address"])
    new_user_home_address = html.escape(data["user_home_address"])
    
    # check if user_id exists
    if not UserTable.query.filter_by(user_id=user_id, user_role='Admin').scalar():
      return abort(404, message="User ID not found.")
    
    # check if user_id already exists, except the current user_id itself
    if UserTable.query.filter(UserTable.user_id == new_user_id, UserTable.user_role == 'Admin', UserTable.user_id != user_id).scalar():
      return abort(400, message="User ID already exists.")
    
    # validate email address
    try:
      validate_email(new_user_email_address)
    except EmailNotValidError as e:
      return abort(400, message=str(e))
    
    # update user_tbl
    admin = UserTable.query.filter_by(user_id=user_id, user_role='Admin').scalar()
    admin.user_id = new_user_id
    admin.user_fullname = new_user_fullname
    admin.user_password_hash = generate_password_hash(new_user_password, method='pbkdf2:sha256')
    admin.user_email_address = new_user_email_address
    admin.user_home_address = new_user_home_address
    
    db.session.commit()
    
    return {"msg": "Admin updated successfully."}, 200
  
  def delete(self, user_id):
    admin = UserTable.query.filter_by(user_id=user_id, user_role='Admin').scalar()
    
    # check if user_id exists
    if not admin:
      return abort(404, message="User ID not found.")
    
    db.session.delete(admin)
    db.session.commit()
    
    return {"msg": "Admin deleted successfully."}, 200


@ns.route('/students/<string:student_uuid>')
class StudentAPI(Resource):
  @ns.marshal_with(student_list_model)
  def get(self, student_uuid):
    query = db.session.query(StudentTable, ClassTable, UserTable, CourseTable) \
            .join(ClassTable, StudentTable.student_class == ClassTable.class_id) \
            .join(UserTable, UserTable.user_id == StudentTable.student_nim) \
            .outerjoin(CourseTable, CourseTable.class_id == ClassTable.class_id) \
            .add_columns(
              StudentTable.student_uuid,
              StudentTable.student_nim,
              StudentTable.student_class,
              UserTable.user_fullname,
              UserTable.user_email_address,
              UserTable.user_home_address,
              StudentTable.date_entry,
              CourseTable.course_id,
              CourseTable.course_name,
              CourseTable.day,
              CourseTable.time_start,
              CourseTable.time_end
            ) \
            .filter(StudentTable.student_uuid == student_uuid) \
            .all()
    
    # check if student_nim exists
    if not query:
      return abort(404, message="Student UUID not found.")
    
    # if the student_nim exist, then return the data
    results = {}
    for data in query:
      student_uuid = data.student_uuid
      
      if student_uuid not in results:
        results[student_uuid] = {
          "student_uuid": student_uuid,
          "student_nim": data.student_nim,
          "student_fullname": data.user_fullname,
          "student_class": data.student_class,
          "student_email_address": data.user_email_address,
          "student_home_address": data.user_home_address,
          "date_entry": data.date_entry,
          "student_courses": []
        }
        
      if data.course_id:
        course_info = {
          "course_id": data.course_id,
          "course_name": data.course_name,
          "day": data.day.value,
          "time_start": str(data.time_start),
          "time_end": str(data.time_end)
        }
        results[student_uuid]["student_courses"].append(course_info)
    
    return list(results.values()), 200

  @ns.expect(student_input_model)
  def put(self, student_uuid):
    data = ns.payload
    
    new_student_nim = html.escape(data["student_nim"])
    new_student_fullname = html.escape(data["student_fullname"])
    new_student_password = data["student_password"]
    new_student_card_uid = data["student_card_uid"]
    new_student_class = html.escape(data["student_class"])
    new_student_email_address = html.escape(data["student_email_address"])
    new_student_home_address = html.escape(data["student_home_address"])
    
    # check if student_uuid exists
    if not StudentTable.query.filter_by(student_uuid=student_uuid).scalar():
      return abort(404, message="Student UUID not found.") # Bad request
    
    # check if student_nim already exists, except the current student_nim
    if StudentTable.query.filter(StudentTable.student_nim == new_student_nim, StudentTable.student_uuid != student_uuid).scalar():
      return abort(400, message="Student NIM already exists.") # Bad request
    
    # check if student_class exists
    if not ClassTable.query.filter_by(class_id=new_student_class).scalar():
      return abort(404, message="Class not found.") # Not found
    
    # validate email address
    try:
      validate_email(new_student_email_address)
    except EmailNotValidError as e:
      return abort(400, message=str(e)) # Bad request
    
    # update user_tbl
    user = UserTable.query.filter_by(user_id=new_student_nim).scalar()
    user.user_id = new_student_nim
    user.user_fullname = new_student_fullname
    user.user_password_hash = generate_password_hash(new_student_password, method='pbkdf2:sha256')
    user.user_rfid_hash = generate_password_hash(new_student_card_uid, method='pbkdf2:sha256')
    user.user_email_address = new_student_email_address
    user.user_home_address = new_student_home_address
    
    # update student_tbl
    student = StudentTable.query.filter_by(student_uuid=student_uuid).scalar()
    student.student_nim = new_student_nim
    student.student_class = new_student_class
    
    db.session.commit()
    
    return {"msg": "Student updated successfully."}, 200
  
  def delete(self, student_uuid):
    student = StudentTable.query.filter_by(student_uuid=student_uuid).scalar()
    
    # check if student_uuid exists
    if not student:
      return abort(404, message="Student UUID not found.")
    
    db.session.delete(student) # delete from student_tbl first
    db.session.delete(UserTable.query.filter_by(user_id=student.student_nim).scalar()) # then, delete from user_tbl
    db.session.commit()
    
    return {"msg": "Student deleted successfully."}, 200


@ns.route('/lecturers/<string:lecturer_uuid>')
class LecturerAPI(Resource):
  @ns.marshal_with(lecturer_list_model)
  def get(self, lecturer_uuid):
    query = db.session.query(LecturerTable, UserTable, CourseTable) \
            .join(UserTable, UserTable.user_id == LecturerTable.lecturer_nip) \
            .outerjoin(CourseTable, CourseTable.lecturer_nip == LecturerTable.lecturer_nip) \
            .add_columns(
              LecturerTable.lecturer_uuid,
              LecturerTable.lecturer_nip,
              UserTable.user_fullname,
              LecturerTable.lecturer_major,
              UserTable.user_email_address,
              UserTable.user_home_address,
              LecturerTable.date_entry,
              CourseTable.course_id,
              CourseTable.course_name,
              CourseTable.day,
              CourseTable.time_start,
              CourseTable.time_end
            ) \
            .filter(LecturerTable.lecturer_uuid == lecturer_uuid) \
            .all()
    
    # check if lecturer_uuid exists
    if not query:
      return abort(404, message="Lecturer UUID not found.")
    
    # if the lecturer_uuid exist, then return the data
    results = {}
    for data in query:
      lecturer_uuid = data.lecturer_uuid
      
      if lecturer_uuid not in results:
        results[lecturer_uuid] = {
          "lecturer_uuid": data.lecturer_uuid,
          "lecturer_nip": data.lecturer_nip,
          "lecturer_fullname": data.user_fullname,
          "lecturer_major": data.lecturer_major.value,
          "lecturer_email_address": data.user_email_address,
          "lecturer_home_address": data.user_home_address,
          "date_entry": data.date_entry,
          "lecturer_courses": []
        }
        
      if data.course_id:
        course_info = {
          "course_id": data.course_id,
          "course_name": data.course_name,
          "day": data.day.value,
          "time_start": str(data.time_start),
          "time_end": str(data.time_end)
        }
        results[lecturer_uuid]["lecturer_courses"].append(course_info)
    
    return list(results.values()), 200
  
  @ns.expect(lecturer_input_model)
  def put(self, lecturer_uuid):
    data = ns.payload
    
    new_lecturer_nip = html.escape(data["lecturer_nip"])
    new_lecturer_fullname = html.escape(data["lecturer_fullname"])
    new_lecturer_password = data["lecturer_password"]
    new_lecturer_card_uid = data["lecturer_card_uid"]
    new_lecturer_major = html.escape(data["lecturer_major"])
    new_lecturer_email_address = html.escape(data["lecturer_email_address"])
    new_lecturer_home_address = html.escape(data["lecturer_home_address"])
    
    # check if lecturer_uuid exists
    if not LecturerTable.query.filter_by(lecturer_uuid=lecturer_uuid).scalar():
      return abort(404, message="Lecturer UUID not found.")
    
    # check if lecturer_nip already exists, except the current lecturer_nip
    if LecturerTable.query.filter(LecturerTable.lecturer_nip == new_lecturer_nip, LecturerTable.lecturer_uuid != lecturer_uuid).scalar():
      return abort(400, message="Lecturer NIP already exists.")
    
    # check if lecturer_major exists
    if not ClassTable.query.filter_by(major=new_lecturer_major).first():
      return abort(404, message="Major not found.")
    
    # validate email address
    try:
      validate_email(new_lecturer_email_address)
    except EmailNotValidError as e:
      return abort(400, message=str(e))
    
    # update user_tbl first
    user = UserTable.query.filter_by(user_id=new_lecturer_nip).scalar()
    user.user_id = new_lecturer_nip
    user.user_fullname = new_lecturer_fullname
    user.user_password_hash = generate_password_hash(new_lecturer_password, method='pbkdf2:sha256')
    user.user_rfid_hash = generate_password_hash(new_lecturer_card_uid, method='pbkdf2:sha256')
    user.user_email_address = new_lecturer_email_address
    user.user_home_address = new_lecturer_home_address
    
    # then, update lecturer_tbl
    lecturer = LecturerTable.query.filter_by(lecturer_uuid=lecturer_uuid).scalar()
    lecturer.lecturer_nip = new_lecturer_nip
    lecturer.lecturer_major = new_lecturer_major
    
    db.session.commit()
    
    return {"msg": "Lecturer updated successfully."}, 200
  
  def delete(self, lecturer_uuid):
    lecturer = LecturerTable.query.filter_by(lecturer_uuid=lecturer_uuid).scalar()
    
    if not lecturer:
      return abort(404, message="Lecturer UUID not found.")
    
    db.session.delete(lecturer) # delete from lecturer_tbl first
    db.session.delete(UserTable.query.filter_by(user_id=lecturer.lecturer_nip).scalar()) # then, delete from user_tbl
    db.session.commit()
    
    return {"msg": "Lecturer deleted successfully."}, 200


@ns.route('/administrators/courses/<string:course_id>')
class CourseAPI(Resource):
  @ns.marshal_with(course_list_model)
  def get(self, course_id):
    query = db.session.query(CourseTable, ClassTable, UserTable, StudentTable) \
            .join(ClassTable, ClassTable.class_id == CourseTable.class_id) \
            .outerjoin(StudentTable, StudentTable.student_class == ClassTable.class_id) \
            .outerjoin(UserTable, UserTable.user_id == StudentTable.student_nim) \
            .add_columns(
              CourseTable.course_id,
              CourseTable.course_name,
              CourseTable.lecturer_nip,
              CourseTable.class_id,
              CourseTable.room_id,
              CourseTable.day,
              CourseTable.time_start,
              CourseTable.time_end,
              CourseTable.course_description,
              StudentTable.student_uuid,
              StudentTable.student_nim,
              UserTable.user_fullname,
              UserTable.user_email_address,
            ) \
            .filter(CourseTable.course_id == course_id) \
            .all()
    
    # check if course_id exists
    if not query:
      return abort(404, message="Course ID not found.")
    
    # if the course_id exist, then return the data
    results = {}
    for data in query:
      course_id = data.course_id
      
      if course_id not in results:
        results[course_id] = {
          "course_id": data.course_id,
          "course_name": data.course_name,
          "lecturer_nip": data.lecturer_nip,
          "class_id": data.class_id,
          "room_id": data.room_id,
          "day": data.day.value,
          "time_start": str(data.time_start),
          "time_end": str(data.time_end),
          "course_description": data.course_description,
          "list_of_students": []
        }
        
      if data.student_uuid:
        student_info = {
          "student_uuid": data.student_uuid,
          "student_nim": data.student_nim,
          "student_fullname": data.user_fullname,
          "student_email_address": data.user_email_address,
        }
        results[course_id]["list_of_students"].append(student_info)
      
    return list(results.values()), 200
  
  @ns.expect(course_input_model)
  def put(self, course_id):
    data = ns.payload
    
    new_course_id = html.escape(data["course_id"])
    new_course_name = html.escape(data["course_name"])
    new_lecturer_nip = html.escape(data["lecturer_nip"])
    new_class_id = html.escape(data["class_id"])
    new_room_id = html.escape(data["room_id"])
    new_day = html.escape(data["day"].capitalize())
    new_time_start = html.escape(data["time_start"])
    new_time_end = html.escape(data["time_end"])
    new_course_description = html.escape(data["course_description"])
    
    # check if course_id exists
    if not CourseTable.query.filter_by(course_id=course_id).scalar():
      return abort(404, message="Course ID not found.")
    
    # check if course_id already exists, except the current course_id itself
    if CourseTable.query.filter(CourseTable.course_id == new_course_id, CourseTable.course_id != course_id).scalar():
      return abort(400, message="Course ID already exists.")
    
    # check if lecturer_nip exists
    if not LecturerTable.query.filter_by(lecturer_nip=new_lecturer_nip).scalar():
      return abort(404, message="Lecturer NIP not found.")
    
    # check if class_id exists
    if not ClassTable.query.filter_by(class_id=new_class_id).scalar():
      return abort(404, message="Class not found.")
    
    # check if room_id exists
    if not RoomTable.query.filter_by(room_id=new_room_id).scalar():
      return abort(404, message="Room not found.")
    
    # check if day is valid
    if new_day not in DAYS_IN_A_WEEK:
      return abort(400, message="Day is not valid.")
    
    # check if time_start and time_end is valid
    try:
      converted_time_start = datetime.strptime(new_time_start, "%H:%M:%S").time()
      converted_time_end = datetime.strptime(new_time_end, "%H:%M:%S").time()
    except ValueError as e:
      return abort(400, message=str(e))
    
    # update course_tbl
    course = CourseTable.query.filter_by(course_id=course_id).scalar()
    course.course_id = new_course_id
    course.course_name = new_course_name
    course.lecturer_nip = new_lecturer_nip
    course.class_id = new_class_id
    course.room_id = new_room_id
    course.day = new_day
    course.time_start = str(converted_time_start)
    course.time_end = str(converted_time_end)
    course.course_description = new_course_description
    
    db.session.commit()
    
    return {"msg": "Course updated successfully."}, 200
  
  def delete(self, course_id):
    course = CourseTable.query.filter_by(course_id=course_id).scalar()
    
    # check if course_id exists
    if not course:
      return abort(404, message="Course ID not found.")
    
    # delete from course_tbl
    db.session.delete(course)
    db.session.commit()
    
    return {"msg": "Course deleted successfully."}, 200
