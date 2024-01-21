from flask import Flask
from datetime import timedelta

from .config import TestingConfig, ProductionConfig
from .extensions import argon2, db, migrate, csrf, mqtt
from .app.views import user_ep, admin_ep, lecturer_ep, student_ep
from .app.models import User, Course

from pytz import timezone
from datetime import datetime

topic = "SmarTendance/ESP32/Attendance"
topicfallback = "SmarTendance/ESP32/AttendanceFallback"


def current_time():
  curr_time = datetime.now(timezone("Asia/Jakarta")).strftime("%H:%M:%S")
  print(curr_time)
  return curr_time

def current_day():
  curr_day = datetime.now(timezone("Asia/Jakarta")).strftime("%A")
  print(curr_day)
  return curr_day


def create_app(testing: bool = True):
	app = Flask(__name__)
	app.permanent_session_lifetime = timedelta(hours=1)
	app.url_map.strict_slashes = False
	# Check for testing parameter value.
	if testing:
		app.config.from_object(TestingConfig)
	else:
		app.config.from_object(ProductionConfig)
	# Connecting extensions to flask app
	argon2.init_app(app)
	db.init_app(app)
	migrate.init_app(app, db)
	csrf.init_app(app)
	mqtt.init_app(app)

	@mqtt.on_connect()
	def handle_connect(client, userdata, flags, rc):
		if rc == 0:
			print("Connected to broker")
			mqtt.subscribe(topic)
		else:
			print("Failed to connect, return code %d\n", rc)

	def do_attendance(uid: str):
		with app.app_context():
			found_user = User.query.filter_by(user_rfid_hash=uid).first()
			print(found_user)
			if found_user is None:
				print(f"User with id {uid} not found")
				mqtt.publish(topicfallback, "101")
			print(found_user.user_role)
			student_courses = []
			lecturer_courses = []
			# Check the user's class id
			if found_user.user_role.value == "STUDENT":
				found_course = Course.query.filter_by(
					class_id=found_user.student_class,
					day=current_day(),
				).first()
				student_courses = found_course
			elif found_user.user_role.value == "LECTURER":
				found_course = Course.query.filter_by(
					lecturer_nip=found_user.user_id,
					day=current_day(),
					time_start=current_time(),
					time_end=current_time(),
				).first()
				lecturer_courses = found_course
			else:
				print(f"Role unknown")

			if not (student_courses or lecturer_courses):
				print(f"User with id {uid} not found in any course")
				mqtt.publish(topicfallback, "102")
			else:
				if found_user.user_role.value == "STUDENT":
					print(f"User with id {uid} found in course {student_courses}")
				elif found_user.user_role.value == "LECTURER":
					print(f"User with id {uid} found in course {lecturer_courses}")

	@mqtt.on_message()
	def handle_mqtt_message(client, userdata, message):
		uid = message.payload.decode("utf-8")
		print("Received message: " + uid)
		print("Received message topic: " + message.topic)

		do_attendance(uid)

	# Registering route or endpoint blueprints
	app.register_blueprint(user_ep)
	app.register_blueprint(admin_ep)
	app.register_blueprint(lecturer_ep)
	app.register_blueprint(student_ep)

	return app
