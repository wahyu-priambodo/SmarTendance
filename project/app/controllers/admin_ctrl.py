from flask import redirect, url_for, render_template, request, flash, session, abort, jsonify, Response
from flask_argon2 import generate_password_hash
from datetime import datetime
from sqlalchemy.orm import joinedload
import pandas as pd
from io import BytesIO

from ..models import *

""" Function helper """
def validate_user_form(
  user_id:str, user_role:str, user_fullname:str, user_pw:str, user_confirm_pw:str, user_email_address:str, user_uid:str, user_home_address:str = None, student_class:str = None,
  lecturer_major:str = None
  ) -> bool:
  # Check if all field is filled
  if not (user_id and user_fullname and user_pw and user_confirm_pw and user_email_address and user_uid):
    flash('Please fill all the form!', 'danger')
    return False
  # Check if user confirm password is same as password
  if not user_pw == user_confirm_pw:
    flash('Confirm password must be same as password!', 'danger')
    return False
  # Check if the user password is valid
  if len(user_pw) < 8:
    flash('Password must be at least 8 characters!', 'danger')
    return False
  # Check if the password contains minimum 1 uppercase, 1 lowercase, 1 number, and 1 symbol
  if not (
    any(char.isupper() for char in user_pw) and 
    any(char.islower() for char in user_pw) and 
    any(char.isdigit() for char in user_pw) and 
    any(not char.isalnum() for char in user_pw)
  ):
    flash('Password must contain minimum 1 uppercase, 1 lowercase, 1 number, and 1 symbol!', 'danger')
    return False
  # Validate user email address
  if not '@' in user_email_address:
    flash('Email address is not valid!', 'danger')
    return False
  # Validate user home address
  if user_home_address:
    if len(user_home_address) > 256:
      flash('Home address must be less than 256 characters!', 'danger')
      return False
  # Validate user role
  if user_role == 'STUDENT':
    # Check if the user id length is 10
    if len(user_id) != 10:
      flash('Student NIM must be 10 characters long!', 'danger')
      return False
    # Check if the student already registered
    student_exist = User.query.filter_by(
      user_id=user_id,
      user_role='STUDENT'
    ).first()
    if student_exist:
      flash('Student already registered!', 'danger')
      return False
    # Check if the student class is valid
    student_class_exist = Class.query.filter_by(
      class_id=student_class
    ).first()
    if not student_class_exist:
      flash('Student class is not valid!', 'danger')
      return False
  elif user_role == 'LECTURER':
    # Check if the lecturer nip length is 18
    if len(user_id) != 18:
      flash('Lecturer NIP must be 18 characters long!', 'danger')
      return False
    # Check if the lecturer already registered
    lecturer_exist = User.query.filter_by(
      user_id=user_id,
      user_role='LECTURER'
    ).first()
    if lecturer_exist:
      flash('Lecturer already registered!', 'danger')
      return False
    # Check if the lecturer major is valid
    lecturer_major_list = [major.value for major in Major]
    if lecturer_major not in lecturer_major_list:
      flash('Lecturer major is not valid!', 'danger')
      return False
  # return True if all validation passed
  return True

def is_valid_day(day: str) -> bool:
  days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
  return day.capitalize() in days_of_week

def is_valid_time(time: str) -> bool:
  try:
    datetime.strptime(time, '%H:%M:%S')
    return True
  except ValueError:
    return False

def validate_course_form(
  course_id:str, course_name:str, course_sks:int, at_semester:int,
  day:str, time_start:str, time_end:str, course_description:str,
  lecturer_nip:str, class_id:str, room_id:str
) -> bool:
  if not (course_id and course_name and course_sks and at_semester 
          and day and time_start and time_end
          and lecturer_nip and class_id and room_id
  ):
    flash('Please fill all the form!', 'danger')
    return False
  if len(course_id) > 15:
    flash('Course ID must be less than 15 characters!', 'danger')
    return False
  if len(course_name) > 100:
    flash('Course name must be less than 100 characters!', 'danger')
    return False
  if not (isinstance(course_sks,int)) or (course_sks<1 or course_sks>=6):
    flash('Course SKS must be between 1 and 8!', 'danger')
    return False
  if not (isinstance(at_semester,int)) or (at_semester<1 or at_semester>=8):
    flash('Course semester must be between 1 and 8!', 'danger')
    return False
  if not is_valid_day(day):
    flash('Day must be a day of week!', 'danger')
    return False
  if time_start == time_end:
    flash('Time start and time end must be different!', 'danger')
    return False
  if not (is_valid_time(time_start) or is_valid_time(time_end)):
    flash('Time start or time end must be in format HH:MM AM/PM!', 'danger')
    return False
  if len(course_description) > 256:
    flash('Course description must be less than 256 characters!', 'danger')
    return False
  # Check for lecturer NIP
  lecturer_exist = User.query.filter_by(
    user_id=lecturer_nip,
    user_role='LECTURER'
  ).first()
  if not lecturer_exist:
    flash('Lecturer NIP is not valid!', 'danger')
    return False
  # Check if course already registered
  course_exist = Course.query.filter_by(course_id=course_id).first()
  if course_exist:
    flash('Course already registered!', 'danger')
    return False
  # Check for class ID
  class_exist = Class.query.filter_by(class_id=class_id).first()
  if not class_exist:
    flash('Class ID is not valid!', 'danger')
    return False
  # Check for room ID
  room_exist = Room.query.filter_by(room_id=room_id).first()
  if not room_exist:
    flash('Room ID is not valid!', 'danger')
    return False
  # return True if all validation passed
  return True

def format_time(time_object:datetime):
  formatted_time = time_object.strftime('%a, %d %b %Y %H:%M:%S')
  return formatted_time
""" End of function helper """

""" Registration """
def add():
  sess_user_id = session.get('user_id')
  sess_user_role = session.get('user_role')
  # Check user session
  if not (sess_user_id and sess_user_role):
    return redirect(url_for('user_ep.login'))
  # Check user role
  if sess_user_role != 'ADMIN':
    return abort(403)
  return render_template('admin/registrasi.html')

def add_student():
  sess_user_id = session.get('user_id')
  sess_user_role = session.get('user_role')
  # Check user session
  if not (sess_user_id and sess_user_role):
    return redirect(url_for('user_ep.login'))
  # Check user role
  if sess_user_role != 'ADMIN':
    return abort(403)
  form = request.form
  student_class = Class.query.all()
  if request.method == 'POST':
    student_name = form['student_name']
    student_nim = form['student_nim']
    student_class = form['student_class']
    student_pw = form['student_pw']
    student_confirm_pw = form['student_confirm_pw']
    student_email_address = form['student_email_address']
    student_home_address = form['student_home_address']
    student_uid = form['student_uid']
    # Validate user form
    is_form_valid = validate_user_form(
      user_id=student_nim, user_role='STUDENT', user_fullname=student_name, user_pw=student_pw, user_confirm_pw=student_confirm_pw, user_email_address=student_email_address, user_uid=student_uid, user_home_address=student_home_address, student_class=student_class
    )
    # Check if the form is valid
    if not is_form_valid:
      return redirect(url_for('admin_ep.add_student'))
    # If the form valid, then add new student to database based on the form input
    new_student = User (
      user_id = student_nim,
      user_role = 'STUDENT',
      user_fullname = student_name,
      user_password_hash = generate_password_hash(student_pw),
      user_rfid_hash = generate_password_hash(student_uid),
      user_email_address = student_email_address,
      user_home_address = student_home_address,
      student_class = student_class
    )
    # Add new student to database
    db.session.add(new_student)
    db.session.commit()
    flash('Student successfully registered!', 'success')
    return redirect(url_for('admin_ep.add'))
  return render_template(
    'admin/regis-mhsw.html',
    student_class=student_class
  )

def add_lecturer():
  sess_user_id = session.get('user_id')
  sess_user_role = session.get('user_role')
  # Check user session
  if not (sess_user_id and sess_user_role):
    return redirect(url_for('user_ep.login'))
  # Check user role
  if sess_user_role != 'ADMIN':
    return abort(403)
  form = request.form
  major_list = [major.value for major in Major]
  if request.method == 'POST':
    lecturer_name = form['lecturer_name']
    lecturer_nip = form['lecturer_nip']
    lecturer_major = form['lecturer_major']
    lecturer_pw = form['lecturer_pw']
    lecturer_confirm_pw = form['lecturer_confirm_pw']
    lecturer_email_address = form['lecturer_email_address']
    lecturer_home_address = form['lecturer_home_address']
    lecturer_uid = form['lecturer_uid']
    print(lecturer_name, lecturer_major, lecturer_nip, lecturer_pw, lecturer_confirm_pw, lecturer_email_address, lecturer_home_address, lecturer_uid)
    is_form_valid = validate_user_form(
      user_id=lecturer_nip, user_role='LECTURER', user_fullname=lecturer_name, user_pw=lecturer_pw, user_confirm_pw=lecturer_confirm_pw, user_email_address=lecturer_email_address, user_uid=lecturer_uid, user_home_address=lecturer_home_address, lecturer_major=lecturer_major
    )
    if not is_form_valid:
      return redirect(url_for('admin_ep.add_lecturer'))
    new_lecturer = User (
      user_id = lecturer_nip,
      user_role = 'LECTURER',
      user_fullname = lecturer_name,
      user_password_hash = generate_password_hash(lecturer_pw),
      user_rfid_hash = generate_password_hash(lecturer_uid),
      user_email_address = lecturer_email_address,
      user_home_address = lecturer_home_address,
      lecturer_major = lecturer_major
    )
    db.session.add(new_lecturer)
    db.session.commit()
    flash('Lecturer successfully registered!', 'success')
    return redirect(url_for('admin_ep.add'))
  return render_template(
    'admin/regis-dosen.html',
    major_list=major_list
  )

def add_course():
  sess_user_id = session.get('user_id')
  sess_user_role = session.get('user_role')
  if not (sess_user_id and sess_user_role):
    return redirect(url_for('user_ep.login'))
  if sess_user_role != 'ADMIN':
    return abort(403)
  list_classes = Class.query.all()
  days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
  lecturers = User.query.filter_by(user_role='LECTURER').all()
  rooms = Room.query.all()
  form = request.form
  if request.method == 'POST':
    course_name = form['course_name']
    course_id = form['course_id']
    course_sks = int(form['course_sks'])
    course_semester = int(form['course_semester'])
    course_day = form['course_day']
    course_start = form['time_start']
    course_end = form['time_end']
    course_description = form['course_description']
    lecturer_nip = form['lecturer_nip']
    class_id = form['class_id']
    room_id = form['room_id']
    # Validate course form
    is_course_form_valid = validate_course_form(
      course_id=course_id, course_name=course_name, course_sks=course_sks, at_semester=course_semester, day=course_day, 
      time_start=course_start, time_end=course_end, course_description=course_description,
      lecturer_nip=lecturer_nip, class_id=class_id, room_id=room_id
    )
    # Check if the form is valid
    if not is_course_form_valid:
      return redirect(url_for('admin_ep.add_course'))
    # If the form valid, then add new course to database based on the form input
    new_course = Course (
      course_id = course_id,
      course_name = course_name,
      course_sks = course_sks,
      at_semester = course_semester,
      day = course_day,
      time_start = course_start,
      time_end = course_end,
      course_description = course_description,
      lecturer_nip = lecturer_nip,
      class_id = class_id,
      room_id = room_id
    )
    # Add new course to database
    db.session.add(new_course)
    db.session.commit()
    flash('Course successfully registered!', 'success')
    return redirect(url_for('admin_ep.add'))
  return render_template(
    'admin/regis-course.html',
    list_classes=list_classes,
    days_of_week=days_of_week,
    lecturers=lecturers,
    rooms=rooms
  )
""" End of registration """

""" Attendance """
# Attendance page
def attendance():
  sess_user_id = session.get('user_id')
  sess_user_role = session.get('user_role')
  if not (sess_user_id and sess_user_role):
    return redirect(url_for('user_ep.login'))
  if sess_user_role != 'ADMIN':
    return abort(403)
  roles = ['STUDENT', 'LECTURER']
  return render_template(
    'admin/rekap_absen.html',
    roles=roles,
  )

def serialized_logs(role:str) -> list:
  serialized_logs = []
  if role == 'STUDENT':
    student_attendance_logs = (
      db.session.query(StudentAttendanceLogs)
      .options(
        joinedload(StudentAttendanceLogs.user_student),
        joinedload(StudentAttendanceLogs.course_student),
        joinedload(StudentAttendanceLogs.room_student)
      )
      .all()
    )
    serialized_logs = [
      {
        'name': log.user_student.user_fullname,
        'course': log.course_student.course_name,
        'room': log.room_student.room_id,
        'time_in': format_time(log.time_in),
        'status': log.status.value
      }
      for log in student_attendance_logs
    ]
  elif role == 'LECTURER':
    lecturer_attendance_logs = (
      db.session.query(LecturerAttendanceLogs)
      .options(
        joinedload(LecturerAttendanceLogs.user_lecturer),
        joinedload(LecturerAttendanceLogs.course_lecturer),
        joinedload(LecturerAttendanceLogs.room_lecturer)
      )
      .all()
    )
    serialized_logs = [
      {
        'name': log.user_lecturer.user_fullname,
        'course': log.course_lecturer.course_name,
        'room': log.room_lecturer.room_id,
        'time_in': format_time(log.time_in),
        'status': log.status.value
      }
      for log in lecturer_attendance_logs
    ]
  else:
    return jsonify({'message': 'User role is not valid!'}), 400
  # Return serialized attendance logs in JSON format
  return serialized_logs

# Function to fetch attendance logs by role
def get_attendance(role:str):
  sess_user_id = session.get('user_id')
  sess_user_role = session.get('user_role')
  if not (sess_user_id and sess_user_role):
    return redirect(url_for('user_ep.login'))
  if sess_user_role != 'ADMIN':
    return abort(403)
  # If the selected role is student
  if role in ['STUDENT', 'LECTURER']:
    attendance_logs = serialized_logs(role=role)
    return jsonify({'attendance': attendance_logs}), 200
  else:
    return jsonify({'message': 'User role is not valid!'}), 400

def export_attendance(role:str):
  sess_user_id = session.get('user_id')
  sess_user_role = session.get('user_role')
  if not (sess_user_id and sess_user_role):
    return redirect(url_for('user_ep.login'))
  if sess_user_role != 'ADMIN':
    return abort(403)
  # Create dataframe from serialized logs
  attendance_logs = serialized_logs(role=role)
  # Create dataframe from serialized logs
  df = pd.DataFrame(attendance_logs)
  # Create a BytesIO buffer to store the Excel file
  excel_buffer = BytesIO()
  # Export dataframe to excel_buffer
  df.to_excel(excel_buffer, index=False, header=True)
  # Set the position of the buffer to the beginning
  excel_buffer.seek(0)
  # Create response object
  response = Response(
    excel_buffer.read(),
    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  )
  output_file = f"{role.lower()}_attendance_logs.xlsx"
  # Add headers to response
  response.headers["Content-Disposition"] = f"attachment; filename={output_file}.xlsx"
  # Return response
  return response
""" End of attendance """

def admin_view(id: str):
  pass

def admin_edit(id: str):
  pass

def admin_delete(id: str):
  pass