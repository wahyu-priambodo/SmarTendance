# SmarTendance V2

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
db.session.add_all([User(user_id='2207421048', user_role='ADMIN', user_fullname='Wahyu Priambodo', user_password_hash=generate_password_hash('WahyuPriambodo1!'), user_email_address='wahyu.priambodo.tik22@mhsw.pnj.ac.id')])

# Ini buat mahasiswa
User(user_id='2207421059', user_role='STUDENT', user_fullname='Cornelius Yuli Rosdianto', user_password_hash=generate_password_hash('CorneliusPassword1!'), user_rfid_hash=generate_password_hash('testcornelrfid'), user_email_address='cornelius.yuli.rosdianto.tik22@mhsw.pnj.ac.id', student_class='TMJ-3B'), User(user_id='2207421031', user_role='STUDENT', user_fullname='Muhammad Khairu Mufid', user_password_hash=generate_password_hash('MufidPassword1!'), user_rfid_hash=generate_password_hash('testmufidrfid'), user_email_address='muhammad.khairu.mufid.tik22@mhsw.pnj.ac.id', student_class='TMJ-3B'),User(user_id='2207421032', user_role='STUDENT', user_fullname='Kevin Alonzo Manuel Bakara', user_password_hash=generate_password_hash('KevinPassword1!'), user_rfid_hash=generate_password_hash('testkevinrfid'), user_email_address='kevin.alonzo.manuel.bakara.tik22@mhsw.pnj.ac.id', student_class='TMJ-3B'), User(user_id='2207421033', user_role='STUDENT', user_fullname='Devina Anggraini', user_password_hash=generate_password_hash('DefinaPassword1!'), user_rfid_hash=generate_password_hash('testdevinarfid'), user_email_address='devina.anggraini.tik22@mhsw.pnj.ac.id', student_class='TMJ-3B'), User(user_id='2207421034', user_role='STUDENT', user_fullname='Alif Rendina Pamungkas', user_password_hash=generate_password_hash('AlifPassword1!'), user_rfid_hash=generate_password_hash('testalifrfid'), user_email_address='alif.rendina.pamungkas.tik22@mhsw.pnj.ac.id', student_class='TMJ-3B'), User(user_id='2207421035', user_role='STUDENT', user_fullname='Ibrahim Alvaro', user_password_hash=generate_password_hash('AlvaroPassword1!'), user_rfid_hash=generate_password_hash('testalvarorfid'), user_email_address='ibrahim.alvaro.tik22@mhsw.pnj.ac.id', student_class='TMJ-3B'), User(user_id='2207421046', user_role='STUDENT', user_fullname='Abdurrahman Ammar Ihsan', user_password_hash=generate_password_hash('AmmarPassword1!'), user_rfid_hash=generate_password_hash('testammarrfid'), user_email_address='abdurrahman.ammar.ihsan.tik22@mhsw.pnj.ac.id', student_class='TMJ-3B'), User(user_id='2207421056', user_role='STUDENT', user_fullname='Muhammad Brian Azura Nixon', user_password_hash=generate_password_hash('BrianPassword1!'), user_rfid_hash=generate_password_hash('testbrianrfid'), user_email_address='muhammad.brian.azura.nixon.tik22@mhsw.pnj.ac.id', student_class='TMJ-3B'), User(user_id='2207421057', user_role='STUDENT', user_fullname='Shaquille Arriza Hidayat', user_password_hash=generate_password_hash('ShaquillePassword1!'), user_rfid_hash=generate_password_hash('testshaquillerfid'), user_email_address='shaquille.arriza.hidayat.tik22@mhsw.pnj.ac.id', student_class='TMJ-3B')

# Ini buat dosen
User(user_id='197509152003122003', user_role='LECTURER', user_fullname='Maria Agustin', user_password_hash=generate_password_hash('MariaPassword1!'), user_rfid_hash=generate_password_hash('testmariarfid'), user_email_address='maria.agustin@tik.pnj.ac.id', lecturer_major='TIK'), User(user_id='197910062003122001', user_role='LECTURER', user_fullname='Prihatin Oktivasari', user_password_hash=generate_password_hash('PrihatinPassword1!'), user_rfid_hash=generate_password_hash('testprihatinrfid'), user_email_address='prihatin.oktivasari@tik.pnj.ac.id', lecturer_major='TIK'), User(user_id='198112012015041001', user_role='LECTURER', user_fullname='Defiana Arnaldy', user_password_hash=generate_password_hash('DefianaPassword1!'), user_rfid_hash=generate_password_hash('testdefianarfid'), user_email_address='defiana.arnaldy@tik.pnj.ac.id', lecturer_major='TIK'), User(user_id='198501292010121003', user_role='LECTURER', user_fullname='Ariawan Andi Suhandana', user_password_hash=generate_password_hash('AndiPassword1!'), user_rfid_hash=generate_password_hash('testandirfid'), user_email_address='ariawan.andi.suhandana@tik.pnj.ac.id', lecturer_major='TIK'), User(user_id='198605222023212032', user_role='LECTURER', user_fullname='Susana Dwi Yulianti', user_password_hash=generate_password_hash('SusanPassword1!'), user_rfid_hash=generate_password_hash('testsusanrfid'), user_email_address='susana.dwiyulianti@tik.pnj.ac.id', lecturer_major='TIK'), User(user_id='198910112018032002', user_role='LECTURER', user_fullname='Ayu Rosyida Zain', user_password_hash=generate_password_hash('AyuPassword1!'), user_rfid_hash=generate_password_hash('testayurfid'), user_email_address='ayu.rosyidazain@tik.pnj.ac.id', lecturer_major='TIK'), User(user_id='199109262019031012', user_role='LECTURER', user_fullname='Asep Kurniawan', user_password_hash=generate_password_hash('AsepPassword1!'), user_rfid_hash=generate_password_hash('testaseprfid'), user_email_address='asep.kurniawan@tik.pnj.ac.id', lecturer_major='TIK'), User(user_id='199206052022032008', user_role='LECTURER', user_fullname='Ratna Widya Iswara', user_password_hash=generate_password_hash('RatnaPassword1!'), user_rfid_hash=generate_password_hash('testratnarfid'), user_email_address='ratna.widya.iswara@tik.pnj.ac.id', lecturer_major='TIK'), User(user_id='199408202022031009', user_role='LECTURER', user_fullname='Iik Muhamad Malik Matin', user_password_hash=generate_password_hash('IikPassword1!'), user_rfid_hash=generate_password_hash('testiikrfid'), user_email_address='iik.muhamad.malik.matin@tik.pnj.ac.id', lecturer_major='TIK')])

db.session.commit()
```

TODO:

- [ ] Add self-signed SSL certificate (ON PRODUCTION)
- [X] Remove trailing slash for each routes / endpoints.
- [X] Add pop-up confirmation while user want to delete or logout
- [ ] Add pop-up notification after admin complete form registration (danger or success)
- [ ] Add AJAX to JS when request data to the flask server.
