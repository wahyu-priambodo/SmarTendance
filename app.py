from flask import Flask, request, render_template

class AttendanceSystem:
    def __init__(self):
        self.app = Flask(__name__)
        self.configure_routes()
    
    def configure_routes(self):
        self.app.add_url_rule('/', view_func=self.index, methods=['GET', 'POST'])
        self.app.add_url_rule('/dosen', view_func=self.login_dosen)
        self.app.add_url_rule('/tutorial', view_func=self.tutorial)

    def index(self):
        nim = None
        password = None
        if request.method == 'POST':
            nim = request.form.get('NIM')
            password = request.form.get('password')
            if nim == '2207421048' and password == '123456':
                # NIM dan kata sandi cocok, arahkan ke halaman dashboard
                return render_template('Dashboard_mahasiswa.html', nim=nim)
            else:
                # NIM dan kata sandi tidak cocok, tampilkan pesan kesalahan
                return render_template('Portal_utama.html', error_message='NIM atau kata sandi salah')
        return render_template('Portal_utama.html', nim=nim, password=password)

    def login_dosen(self):
        return render_template('Login_dsn.html')
    
    def tutorial(self):
        return render_template('Tutorial.html')
    
    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    app = AttendanceSystem()
    app.run()