from flask import redirect, url_for, render_template, request, flash, session

from ..models import User, Course, Class

def dashboard():
  sess_user_id = session.get('user_id')
  sess_user_role = session.get('user_role')
  if not (sess_user_id and sess_user_role):
    return redirect(url_for('user_ep.login'))
  if sess_user_role == 'ADMIN':
    admin = User.query.filter_by(user_id=sess_user_id, user_role='ADMIN').first()
    students = User.query.filter_by(user_role='STUDENT').all()
    lecturers = User.query.filter_by(user_role='LECTURER').all()
    total_students = len(students)
    total_lecturers = len(lecturers)
    total_courses = len(Course.query.all())
    total_classes = len(Class.query.all())
    # Get total course each student
    student_courses = {}
    for student in students:
      student_courses[student.user_id] = len(
        Course.query.filter_by(class_id=student.student_class).all()
      )
    lecturer_courses = {}
    for lecturer in lecturers:
      lecturer_courses[lecturer.user_id] = len(
        Course.query.filter_by(lecturer_nip=lecturer.user_id).all()
      )
    return render_template(
      'admin/index.html',
      admin=admin,
      students=students,
      lecturers=lecturers,
      total_students=total_students,
      total_lecturers=total_lecturers,
      total_courses=total_courses,
      total_classes=total_classes,
      student_courses=student_courses,
      lecturer_courses=lecturer_courses
    )
  elif sess_user_role == 'LECTURER':
    return render_template('lecturer/index.html')
  else:
    return render_template('student/index.html')

def course():
    sess_user_id = session.get('user_id')
    sess_user_role = session.get('user_role')
    
    if not (sess_user_id and sess_user_role and sess_user_role == 'STUDENT'):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('dashboard'))

    user_courses = Course.query.filter_by(student_id=sess_user_id).all()

    return render_template('student/course.html', user_courses=user_courses)