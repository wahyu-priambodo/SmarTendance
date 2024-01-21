from flask import redirect, url_for, render_template, request, flash, session, abort, jsonify, Response
from flask_argon2 import generate_password_hash
from datetime import datetime
from sqlalchemy.orm import joinedload
import pandas as pd
from io import BytesIO

from ..models import *

# function helper
def format_time(time_object:datetime):
  formatted_time = time_object.strftime('%a, %d %b %Y %H:%M:%S')
  return formatted_time
# end function helper

""" LECTURER ATTENDANCE LOGS """
def serialized_lecturer_logs(lecturer_nip:str, course_id:str = None) -> list:
    serialized_lecturer_logs = [] # Empty list to store serialized courses
    lecturer_logs = db.session.query(LecturerAttendanceLogs).options (
        joinedload(LecturerAttendanceLogs.user_lecturer),
        joinedload(LecturerAttendanceLogs.course_lecturer)
    )
    if course_id:
        lecturer_logs = lecturer_logs.filter_by(course_id=course_id)
    lecturer_logs = lecturer_logs.filter_by(lecturer_nip=lecturer_nip).all()
    serialized_lecturer_logs = [
        {
            'log_id': log.log_id,
            'name': log.user_lecturer.user_fullname,
            'course': log.course_lecturer.course_name,
            'room': log.room_id,
            'time_in': format_time(log.time_in),
            'status': log.status.value
        }
        for log in lecturer_logs
    ]
    print(serialized_lecturer_logs)

    return serialized_lecturer_logs

def get_lecturer_logs():
    sess_user_id = session.get('user_id')
    sess_user_role = session.get('user_role')
    if not (sess_user_id and sess_user_role):
        return redirect(url_for('user_ep.login'))
    found_lecturer = User.query.filter_by(
        user_id=sess_user_id,
        user_role='LECTURER'
    )
    if (not found_lecturer) and (sess_user_role != 'LECTURER'):
        return abort(403)
    course_id = request.args.get('course_id')
    lecturer_logs = serialized_lecturer_logs(
        lecturer_nip=sess_user_id,
        course_id=course_id
    )
    return jsonify({'logs': lecturer_logs}), 200

def view_lecturer_logs():
    sess_user_id = session.get('user_id')
    sess_user_role = session.get('user_role')
    if not (sess_user_id and sess_user_role):
        return redirect(url_for('user_ep.login'))
    found_lecturer = User.query.filter_by(
        user_id=sess_user_id,
        user_role='LECTURER'
    )
    if (not found_lecturer) and (sess_user_role != 'LECTURER'):
        return abort(403)
    courses = Course.query.filter_by(lecturer_nip=sess_user_id).all()
    return render_template(
        'lecturer/rekap_absen_dsn.html',
        courses=courses
    )

def export_lecturer_logs():
    sess_user_id = session.get('user_id')
    sess_user_role = session.get('user_role')
    if not (sess_user_id and sess_user_role):
        return redirect(url_for('user_ep.login'))
    found_lecturer = User.query.filter_by(
        user_id=sess_user_id,
        user_role='LECTURER'
    )
    if (not found_lecturer) and (sess_user_role != 'LECTURER'):
        return abort(403)
    lecturer_nip = sess_user_id
    course_id = request.args.get('course_id')
    lecturer_logs = serialized_lecturer_logs(
        lecturer_nip=lecturer_nip,
        course_id=course_id
    )
    # Create dataframe from serialized logs
    df = pd.DataFrame(lecturer_logs)
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
    output_file = f"{lecturer_nip}_attendance_logs.xlsx"
    # Add headers to response
    response.headers["Content-Disposition"] = f"attachment; filename={output_file}"
    # Return response
    return response

""" STUDENT ATTENDANCE LOGS """
def serialized_student_logs(selected_course:str, student_nim:str=None) -> list:
    """
    This function is for serializing or converting user attendance logs based on selected role and selected course id in JSON format.
    Required param: selected_course (str)
    Optional params:
        - student_nim (str)
    """
    # A list to store serialized logs (in JSON format)
    serialized_student_logs = []

    if selected_course:
        student_logs = db.session.query(StudentAttendanceLogs).options(
            joinedload(StudentAttendanceLogs.user_student),
            joinedload(StudentAttendanceLogs.course_student),
            joinedload(StudentAttendanceLogs.room_student)
        )

        # Check if student_nim is passed in query string
        if student_nim:
            student_logs = student_logs.filter_by(student_nim=student_nim)

        # Filter student attendance logs based on selected_course
        student_logs = student_logs.filter_by(course_id=selected_course).all()

        # Serialize student attendance logs
        serialized_student_logs = [
            {
                'log_id': log.log_id,
                'nim': log.user_student.user_id,
                'name': log.user_student.user_fullname,
                'course': log.course_student.course_name,
                'room': log.room_student.room_id,
                'time_in': format_time(log.time_in),
                'status': log.status.value
            }
            for log in student_logs
        ]
    else:
        return jsonify({'message': 'Course ID must be provided!'}), 400

    # Return the serialized attendance logs
    return serialized_student_logs

def get_student_logs():
    sess_user_id = session.get('user_id')
    sess_user_role = session.get('user_role')
    # Check user session
    if not (sess_user_id and sess_user_role):
        return redirect(url_for('user_ep.login'))
    # Check user role
    if sess_user_role != 'LECTURER':
        return abort(403)

def view_student_logs():
    sess_user_id = session.get('user_id')
    sess_user_role = session.get('user_role')
    # Check user session
    if not (sess_user_id and sess_user_role):
        return redirect(url_for('user_ep.login'))
    # Check user role
    if sess_user_role != 'LECTURER':
        return abort(403)
    courses = Course.query.filter_by(lecturer_nip=sess_user_id).all()
    print(sess_user_id)
    return render_template(
        'lecturer/rekap_absen_mhs.html',
        courses=courses
    )

def student_recap():
    sess_user_id = session.get('user_id')
    sess_user_role = session.get('user_role')
    # Check user session
    if not (sess_user_id and sess_user_role):
        return redirect(url_for('user_ep.login'))
    # Check user role
    if sess_user_role != 'LECTURER':
        return abort(403)
    courses = Course.query.filter_by(lecturer_nip=sess_user_id).all()
    print(sess_user_id)
    return render_template(
        'lecturer/rekap_absen_mhs.html',
        courses=courses
    )


