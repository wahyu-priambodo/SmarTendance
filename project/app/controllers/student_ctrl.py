from flask import redirect, url_for, render_template, request, flash, session, abort
from flask_argon2 import generate_password_hash
from datetime import datetime

from ..models import *

""" Function helper """
def course():
    sess_user_id = session.get('user_id')
    sess_user_role = session.get('user_role')
    
    if not (sess_user_id and sess_user_role and sess_user_role == 'STUDENT'):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('dashboard'))

    student = User.query.filter_by(user_id=sess_user_id).first()
    student_courses = Course.query.filter_by(class_id=student.student_class).all()
    lecturers_nip = [course.lecturer_nip for course in student_courses]
    lecturer = User.query.filter_by(user_id=lecturers_nip, user_role='LECTURER').first() 
    return render_template('student/course.html', student_courses=student_courses, lecturer=lecturer)
      
        
  