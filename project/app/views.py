from flask import Blueprint

from .controllers.user_ctrl import *
from .controllers.admin_ctrl import *
from .controllers.lecturer_ctrl import *
from .controllers.student_ctrl import *

# Creating endpoint blueprints for each user (from general to specific)
user_ep = Blueprint('user_ep', __name__)
admin_ep = Blueprint('admin_ep', __name__, url_prefix='/admin')
lecturer_ep = Blueprint('lecturer_ep', __name__, url_prefix='/lecturer')
student_ep = Blueprint('student_ep', __name__, url_prefix='/student')

# List of user endpoints (general routes)
user_ep.add_url_rule('/', endpoint="index", view_func=index, methods=['GET'])
user_ep.add_url_rule('/login', endpoint="login", view_func=login, methods=['GET', 'POST'])
user_ep.add_url_rule('/logout', endpoint="logout", view_func=logout, methods=['GET'])
user_ep.add_url_rule('/dashboard', endpoint="dashboard", view_func=dashboard, methods=['GET'])

# List of admin endpoints (admin routes)
# Action for registation (insert/add)
admin_ep.add_url_rule('/add', endpoint="add", view_func=add, methods=['GET'])
admin_ep.add_url_rule('/add/student', endpoint="add_student", view_func=add_student, methods=['GET', 'POST'])
admin_ep.add_url_rule('/add/lecturer', endpoint="add_lecturer", view_func=add_lecturer, methods=['GET', 'POST'])
admin_ep.add_url_rule('/add/course', endpoint="add_course", view_func=add_course, methods=['GET', 'POST'])

admin_ep.add_url_rule('/<string:id>/view', endpoint="view", view_func=admin_view, methods=['GET'])
admin_ep.add_url_rule('/<string:id>/edit', endpoint="edit", view_func=admin_edit, methods=['GET', 'POST'])
admin_ep.add_url_rule('/<string:id>/delete', endpoint="delete", view_func=admin_delete, methods=['GET', 'POST'])

# List of lecturer endpoints (lecturer routes)
# Lecturer only can edit student attendance
lecturer_ep.add_url_rule('/<string:id>/edit', endpoint="lecturer_edit", view_func="edit", methods=['GET', 'POST'])

# List of student endpoints (student routes)
# Student only can view their attendance
student_ep.add_url_rule('/<string:id>/view', endpoint="student_view", view_func="view", methods=['GET', 'POST'])