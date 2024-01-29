from flask import Flask
from datetime import datetime, timedelta, time
import pytz

from .config import TestingConfig, ProductionConfig
from .extensions import argon2, db, migrate, csrf, mqtt
from .app.views import user_ep, admin_ep, lecturer_ep, student_ep
from .app.models import *

LOCAL_TZ = 'Asia/Jakarta'
SUB_TOPIC = 'SmarTendance/ESP32/Attendance'
PUB_TOPIC = 'SmarTendance/ESP32/Attendance/Response'

def curr_time():
  local_timezone = pytz.timezone(LOCAL_TZ)
  localized_time = datetime.now(local_timezone)
  return localized_time.strftime("%H:%M:%S")

def curr_day():
  jakarta_timezone = pytz.timezone(LOCAL_TZ)
  localized_time = datetime.now(jakarta_timezone)
  return localized_time.strftime("%A")

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
  # Handle MQTT connection
  @mqtt.on_connect()
  def handle_connect(client, userdata, flags, rc):
    if rc == 0:
      print("Connected to broker")
      mqtt.subscribe(SUB_TOPIC)
    else:
      print("Failed to connect, return code %d\n", rc)


  # Function to take attendance (store attendance to db)
  def do_attendance(uid: str) -> bool:
    current_time = datetime.now().time()
    found_user = User.query.filter_by(user_rfid_hash=uid).first()
    if not found_user:
      mqtt.publish(PUB_TOPIC, payload=f"User with id {uid} not found")
      return False
    # Empty list to store student and lecturer courses
    found_course = []
    # Check the user's class id
    if found_user.user_role.value == "STUDENT":
      found_course = Course.query.filter_by(
        class_id=found_user.student_class,
        day=curr_day()
      ).first()
      found_room = found_course.room_id
      print(found_course)
      # PRESENT if under 30 minutes after time_start
      if current_time > found_course.time_start and current_time < found_course.time_end:
        status = "PRESENT"
      else:
        status = "ALPHA"
      mqtt.publish(PUB_TOPIC, payload="Success")

      print("Test")
      print(datetime.now().time() > found_course.time_start)

      new_student_log = StudentAttendanceLogs (
        student_nim=found_user.user_id,
        course_id=found_course.course_id,
        room_id=found_room,
        time_in=datetime.now(),
        status=status
      )
      db.session.add(new_student_log)
      db.session.commit()
    elif found_user.user_role.value == "LECTURER":
      found_course = Course.query.filter_by(
        lecturer_nip=found_user.user_id,
        day=curr_day()
      ).first()
      print(found_course)
    else:
      mqtt.publish(PUB_TOPIC, payload="Role unknown")
      return False

    # Insert attendance to db

    
  # Handle MQTT message
  @mqtt.on_message()
  def handle_mqtt_message(client, userdata, msg):
    uid = msg.payload.decode("utf-8")
    print("Received message: " + uid)
    print("Received message topic: " + msg.topic)
    # Do attendanec based on the user rfid
    with app.app_context():
      do_attendance(uid)
  # Handle MQTT disconnect
  @mqtt.on_disconnect()
  def handle_disconnect(client, userdata, rc):
    print("Disconnected from broker")
  # Handle MQTT error
  @mqtt.on_log()
  def handle_logging(client, userdata, level, buf):
    print("MQTT log: " + buf)
  # Registering route or endpoint blueprints
  app.register_blueprint(user_ep)
  app.register_blueprint(admin_ep)
  app.register_blueprint(lecturer_ep)
  app.register_blueprint(student_ep)
  
  return app