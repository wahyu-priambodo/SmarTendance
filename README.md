git merge origin/wahyu
git push -u origin wahyu
git switch wahyu

List Endpoint:
admin:

```text
- admin/<nim>/edit
- admin/<nip>/edit
- admin/<course_id>/edit
- admin/<course_id>/view
- admin/<nim>/delete
- admin/<nip>/delete
- admin/<course_id>/delete
- admin/new -> admin/new/student
- admin/new -> admin/new/lecturer
- admin/new -> admin/new/course
- admin/show/students
- admin/show/lecturers
- admin/show/courses
```

students

```text
- student/
```

Libraries:
setuptools gunicorn python-dotenv Flask Flask-SQLAlchemy PyMySQL Flask-Migrate Flask-SocketIO Flask-WTF email-validator Flask-Argon2

Kalo gak bisa rename database di phpmyadmin, coba repair table dulu

```python
from flask_argon2 import check_password_hash, generate_password_hash
db.session.add_all([
User(user_id='1234567890', user_role='ADMIN', user_fullname='Admin Satu', user_password_hash=generate_password_hash(
'AdminPassword1!'), user_rfid_hash=generate_password_hash('testadmin1rfid'), user_email_address='admin1@tik.pnj.ac.id')
])
from flask_argon2 import check_password_hash, generate_password_hash
db.session.add_all([User(user_id='2207421048', user_role='ADMIN', user_fullname='Wahyu Priambodo', user_password_hash=generate_password_hash('WahyuPriambodo1!'), user_email_address='wahyu.priambodo.tik22@mhsw.pnj.ac.id'), User(user_id='2207421059', user_role='STUDENT', user_fullname='Cornelius Yuli Rosdianto', user_password_hash=generate_password_hash('CorneliusPassword1!'), user_rfid_hash=generate_password_hash('testcornelrfid'), user_email_address='cornelius.yuli.rosdianto.tik22@mhsw.pnj.ac.id', student_class='TMJ-3B')])
db.session.commit()
db.session.commit()
```