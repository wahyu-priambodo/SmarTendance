from flask import redirect, url_for, render_template, request, flash, session, abort
from flask_argon2 import generate_password_hash
from datetime import datetime

from ..models import *

def lecturer_edit():
    sess_user_id = session.get('user_id')
    sess_user_role = session.get('user_role')
    # Check user session
    if not (sess_user_id and sess_user_role):
        return redirect(url_for('user_ep.login'))
    # Check user role
    if sess_user_role != 'LECTURER':
        return abort(403)
    return render_template('lecturer/rekap_absen_mhs.html')

def lecturer_view():
    sess_user_id = session.get('user_id')
    sess_user_role = session.get('user_role')
    # Check user session
    if not (sess_user_id and sess_user_role):
        return redirect(url_for('user_ep.login'))
    # Check user role
    if sess_user_role != 'LECTURER':
        return abort(403)
    return render_template('lecturer/rekap_absen_dsn.html')
