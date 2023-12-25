# from sqlalchemy import event
# from sqlalchemy.exc import IntegrityError
# from werkzeug.security import check_password_hash, generate_password_hash
from enum import Enum

from ..extensions import db

# List study program for class model.
class StudyProgramList(Enum):
  TMJ = 'TMJ'
  TKJ = 'TKJ'
  TI = 'TI'
  TMD = 'TMD'
  TICK = 'TICK'

# List class major for class and lecturer model.
class MajorList(Enum):
  TIK = 'TIK'
  TGP = 'TGP'
  TE = 'TE'
  TS = 'TS'
  TM = 'TM'

# Class model.
class ClassTable(db.Model):
  __tablename__ = 'class_tbl'

  class_id = db.Column(db.String(10), primary_key=True, nullable=False)
  major = db.Column(db.Enum(MajorList), nullable=False)
  study_program = db.Column(db.Enum(StudyProgramList), nullable=False)
  
  # relationships
  students = db.relationship('StudentTable', backref='student_ref_class', foreign_keys='StudentTable.student_class')
  courses = db.relationship('CourseTable', backref='course_ref_class', foreign_keys='CourseTable.class_id')
  
  def __repr__(self):
    return '<Class {}>'.format(self.class_id)

# Room building list for room model.
class RoomBuildingList(Enum):
  GSG = 'GSG'
  AA = 'AA'

# Room model.
class RoomTable(db.Model):
  __tablename__ = 'room_tbl'

  room_id = db.Column(db.CHAR(10), primary_key=True, nullable=False)
  room_building = db.Column(db.Enum(RoomBuildingList), nullable=False)
  room_description = db.Column(db.Text, nullable=True)
  
  # relationships
  courses = db.relationship('CourseTable', backref='course_ref_room', foreign_keys='CourseTable.room_id')
  lecturer_attendance_logs = db.relationship('LecturerAttendanceLogTable', backref='lecturer_logs_ref_room', foreign_keys='LecturerAttendanceLogTable.room_id')
  student_attendance_logs = db.relationship('StudentAttendanceLogTable', backref='student_logs_ref_room', foreign_keys='StudentAttendanceLogTable.room_id')

  def __repr__(self):
    return '<Room {}>'.format(self.room_id)

# Roles for user model.
class Roles(Enum):
  Admin = 'Admin'
  Lecturer = 'Lecturer'
  Student = 'Student'

# User model.
class UserTable(db.Model):
  __tablename__ = "user_tbl"

  user_id = db.Column(db.String(25), primary_key=True, nullable=False)
  user_fullname = db.Column(db.String(50), nullable=False)
  user_password_hash = db.Column(db.String(255), nullable=False)
  user_rfid_hash = db.Column(db.String(255), unique=True, nullable=True)
  user_role = db.Column(db.Enum(Roles), nullable=False)
  user_email_address = db.Column(db.String(100), unique=True, nullable=False)
  user_home_address = db.Column(db.Text, nullable=True)

  # relationships
  students = db.relationship('StudentTable', backref='student_ref_user', foreign_keys='StudentTable.student_nim')
  lecturers = db.relationship('LecturerTable', backref='lecturer_ref_user', foreign_keys='LecturerTable.lecturer_nip')
  lecturer_courses = db.relationship('CourseTable', backref='course_ref_user', foreign_keys='CourseTable.lecturer_nip')
  lecturer_attendance_logs = db.relationship('LecturerAttendanceLogTable', backref='lecturer_logs_ref_user', foreign_keys='LecturerAttendanceLogTable.lecturer_nip')
  student_attendance_logs = db.relationship('StudentAttendanceLogTable', backref='student_logs_ref_user', foreign_keys='StudentAttendanceLogTable.student_nim')

  def __repr__(self):
    return '<User {}>'.format(self.user_id)

# Student model.
class StudentTable(db.Model):
  __tablename__ = 'student_tbl'

  student_uuid = db.Column(db.String(36), primary_key=True, nullable=False)
  student_nim = db.Column(db.String(25), db.ForeignKey('user_tbl.user_id'), nullable=False)
  student_class = db.Column(db.String(10), db.ForeignKey('class_tbl.class_id'), nullable=False)
  date_entry = db.Column(db.DATE, nullable=False)

  def __repr__(self):
    return '<Student {}>'.format(self.student_uuid)

# Lecturer model.
class LecturerTable(db.Model):
  __tablename__ = 'lecturer_tbl'

  lecturer_uuid = db.Column(db.String(36), primary_key=True, nullable=False)
  lecturer_nip = db.Column(db.String(25), db.ForeignKey('user_tbl.user_id'), nullable=False)
  lecturer_major = db.Column(db.Enum(MajorList), nullable=False)
  date_entry = db.Column(db.DATE, nullable=False)

  def __repr__(self):
    return '<Lecturer {}>'.format(self.lecturer_uuid)

# Weeks for course model.
class Days(Enum):
  Monday = 'Monday'
  Tuesday = 'Tuesday'
  Wednesday = 'Wednesday'
  Thursday = 'Thursday'
  Friday = 'Friday'
  Saturday = 'Saturday'

# Course model.
class CourseTable(db.Model):
  __tablename__ = "course_tbl"

  course_id = db.Column(db.CHAR(10), primary_key=True, nullable=False)
  course_name = db.Column(db.String(100), unique=True, nullable=False)
  lecturer_nip = db.Column(db.String(25), db.ForeignKey('user_tbl.user_id'), nullable=False)
  class_id = db.Column(db.String(10), db.ForeignKey('class_tbl.class_id'), nullable=False)
  room_id = db.Column(db.String(10), db.ForeignKey('room_tbl.room_id'), nullable=False)
  day = db.Column(db.Enum(Days), nullable=False)
  time_start = db.Column(db.TIME, nullable=False)
  time_end = db.Column(db.TIME, nullable=False)
  course_description = db.Column(db.Text, nullable=True)

  def __repr__(self):
    return '<Course {}>'.format(self.course_id)

# Lecturer attendance log model.
class LecturerAttendanceLogTable(db.Model):
  __tablename__ = "lecturer_attendance_log_tbl"

  log_id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
  lecturer_nip = db.Column(db.String(25), db.ForeignKey('user_tbl.user_id'), nullable=False)
  course_id = db.Column(db.String(10), db.ForeignKey('course_tbl.course_id'), nullable=False)
  room_id = db.Column(db.String(10), db.ForeignKey('room_tbl.room_id'), nullable=False)
  day = db.Column(db.Enum(Days), nullable=False)
  time_in = db.Column(db.TIMESTAMP, nullable=False)
  time_out = db.Column(db.TIMESTAMP, nullable=False)

  def __repr__(self):
    return '<LecturerAttendanceLog {}>'.format(self.log_id)

# Attendance status for student attendance log model.
class AttendanceStatus(Enum):
  Present = 'Present'
  Late = 'Late'
  Alpha = 'Alpha'

# Student attendance log model.
class StudentAttendanceLogTable(db.Model):
  __tablename__ = "student_attendance_log_tbl"

  log_id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
  student_nim = db.Column(db.String(25), db.ForeignKey('user_tbl.user_id'), nullable=False)
  course_id = db.Column(db.String(10), db.ForeignKey('course_tbl.course_id'), nullable=False)
  room_id = db.Column(db.String(10), db.ForeignKey('room_tbl.room_id'), nullable=False)
  status = db.Column(db.Enum(AttendanceStatus), nullable=False)
  time_in = db.Column(db.TIMESTAMP, nullable=False)
  time_out = db.Column(db.TIMESTAMP, nullable=False)
  day = db.Column(db.Enum(Days), nullable=False)

  def __repr__(self):
    return '<StudentAttendanceLog {}>'.format(self.log_id)