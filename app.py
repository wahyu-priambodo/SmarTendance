from flask import Flask, request, render_template

class AttendanceSystem:
  # Daftar user
  users = [
    {
      'Nama': 'Wahyu Priambodo',
      'NIM': '2207421048',
      'Password': '123456'
    },
    {
      'Nama': 'Muhammad Khairu Mufid',
      'NIM': '2207421039',
      'Password': '12345678'
    }
  ]

  def __init__(self):
    self.app = Flask(__name__)
    self.configure_routes()

  def configure_routes(self):
    self.app.add_url_rule('/', view_func=self.index)
    self.app.add_url_rule('/dosen', view_func=self.login_dosen)
    self.app.add_url_rule('/tutorial', view_func=self.tutorial)
    self.app.add_url_rule('/dashboard', view_func=self.dashboard, methods=['GET'])

  def index(self):
    return render_template('Portal_utama.html')

  def login_dosen(self):
    return render_template('Login_dsn.html')

  def dashboard(self):
    nim = request.args.get('NIM')
    password = request.args.get('Password')
    
    for user in self.users:
      if user['NIM'] == nim and user['Password'] == password:
        return render_template('Dashboard.html', nama=user['Nama'])
    else:
      return "NIM atau Password salah"

  def tutorial(self):
    return render_template('Tutorial.html')

  def run(self):
    self.app.run(debug=True)

if __name__ == '__main__':
  app = AttendanceSystem()
  app.run()