# 🚀 Backend v1.0 Has Released! 🚀
- Changing from PHP (native) to Flask Python (3.0.0)
- Using REST API architecture (using flask-restx)
- REST API docs can be accessed at `/api/v1/docs` endpoint 

## 💻 Development Environment 💻
Backend     : Python **3.10.12**, Flask **3.0.0**
Database    : SQLite3 **3.38.5**
Tested OS   : Ubuntu Desktop 22.04 LTS 
Status code :

```txt
200 -> Successfully send request
201 -> Successfully create new data
400 -> bad request (invalid syntax)
401 -> unauthorized
403 -> access forbidden
404 -> not found
405 -> method not allowed
```

## 🚧 Usage 🚧
```shell
source .venv/bin/activate # activate venv
pip3 -r requirements.txt  # install all requirements
flask run                 # run flask app
```

## 🐍 Customizations 🐍
```python
# To generate your own `JWT_SECRET_KEY` use this command:
import secrets
print(secrets.token_hex())
# copy the result to your .flaskenv file and replace the value of `JWT_SECRET_KEY` variable.
```

## 👇 Credits 👇
- ChatGPT
- Pretty Printed YouTube Channel

### 📋 TODO 📋
[X] Buat semua api endpoint (DONE)
[ ] Proteksi REST server dengan JWT (flask_jwt_extended)
[ ] Menerapkan role-based authorization pada protected endpoint
[ ] Menambahkan salt untuk password lecturer dan student
[ ] Membatasi presensi 1 kali per-pertemuan (per-minggu)