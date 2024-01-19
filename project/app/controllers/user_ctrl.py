from flask import redirect, url_for, render_template, request, flash, session

from ..models import User, Course, Class, StudentAttendanceLogs
def index():
  return redirect(url_for('user_ep.login'))

def login():
  sess_user_id = session.get('user_id')
  sess_user_role = session.get('user_role')
  if sess_user_id and sess_user_role:
    return redirect(url_for('user_ep.dashboard'))
  # create login form
  form = request.form
  if request.method == 'POST':
    user_id = form['user_id']
    user_pw = form['user_pw']
    # Check for existing user
    found_user = User.query.filter_by(user_id=user_id).first()
    if found_user and found_user.verify_password(user_pw):
      session['user_id']=found_user.user_id
      session['user_role']=found_user.user_role.value
      flash('Login success!', 'success')
      return redirect(url_for('user_ep.dashboard'))
    else:
      flash('Login failed. Invalid id or password!', 'danger')
      return redirect(url_for('user_ep.login'))
  return render_template('user/login.html')

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
        sess_user_id = session.get('user_id')
        sess_user_role = session.get('user_role')
        
        if not (sess_user_id and sess_user_role):
            return redirect(url_for('user_ep.login'))
        
        if sess_user_role == 'LECTURER':
            lecturer = User.query.filter_by(user_id=sess_user_id, user_role='LECTURER').first()

            # Fetch data for the lecturer
            courses = Course.query.filter_by(lecturer_nip=lecturer.user_id).all()


            # Fetch students based on the class IDs
            students = User.query.join(Class, User.student_class == Class.class_id)\
                                  .join(Course, Course.class_id == Class.class_id)\
                                  .filter(Course.course_id.in_([course.course_id for course in courses]))\
                                  .distinct(User.user_id).all()

            student = (
                  User.query
                  .filter((User.user_role == 'STUDENT') & (User.user_id == sess_user_id))
                  .join(Course, Course.class_id == User.student_class)
                  .filter(Course.lecturer_nip == sess_user_id)
                  .add_columns(User.user_fullname, User.user_id, User.student_class, Course.course_name)
                  .first()
              )

            return render_template('lecturer/index.html', lecturer=lecturer, students=students, courses=courses)
        
        # Handle other roles or redirect as needed
        return render_template('index.html')
    else:
        student = User.query.filter_by(user_id=sess_user_id).first()
        student_courses = Course.query.filter_by(class_id=student.student_class).all()
        lecturers_nip = [course.lecturer_nip for course in student_courses]
        lecturer = User.query.filter_by(user_id=lecturers_nip, user_role='LECTURER').first()

        # Fetch student attendance logs for each course
        attendance_data = {}
        for course in student_courses:
            attendance_logs = StudentAttendanceLogs.query.filter_by(student_nim=student.user_id, course_id=course.course_id).all()
            attendance_data[course.course_id] = attendance_logs

        return render_template('student/index.html', student=student, student_courses=student_courses, lecturer=lecturer, attendance_data=attendance_data)

def tutorial():
  return render_template('user/tutorial.html')
  
def logout():
  session.pop('user_id', None)
  session.pop('user_role', None)
  flash('Logout success!', 'success')
  return redirect(url_for('user_ep.login'))