from flask import Blueprint, render_template, url_for, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from ..models import User
from .. import db

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    newPassword = request.form.get('newPassword')
    confirmPassword = request.form.get('confirmPassword')
    auth = "0"
    state = "1"

    if email == "" or name == "" or newPassword == "" or confirmPassword == "":
        flash('請填寫所有欄位', category='error')
        print('Please fill in all fields!')

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email已存在', category='error')
        print('User already exists!')

    new_user = User(email=email, name=name, password=generate_password_hash(newPassword), auth=auth, state=state)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('loginPassword')
    remember = True if request.form.get('remember') else False

    if email == "" or password == "":
        flash('請填寫所有欄位', category='error')
        print('Please fill in all fields!')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Email或密碼錯誤', category='error')
        print('Invalid email or password')
        return redirect(url_for('auth.login'))

    if user.state == "0":
        flash('此帳號已被停權', category='error')
        print('This account has been suspended')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('user.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))