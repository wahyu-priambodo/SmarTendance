from flask import redirect, url_for, render_template, request, flash, session, abort
from flask_argon2 import generate_password_hash

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

def admin_view(id: str):
  pass

def admin_edit(id: str):
  pass

def admin_delete(id: str):
  pass