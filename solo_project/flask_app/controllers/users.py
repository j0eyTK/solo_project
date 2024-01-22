from flask import Flask, render_template, session, redirect, flash, request
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.lift import Lift

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/user/register', methods=['POST'])
def user_register():

    if (User.validate_reg(request.form)):
        User.create({
            "name":request.form['name'],
            "email":request.form['email'],
            "password":request.form['password'],
        })

    return redirect('/')

@app.route('/user/login', methods = ['POST'])
def login():
    user = User.get_by_email(request.form['email'])

    if not user or not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid User", "login")
        return redirect ('/')
    
    session['user_id'] = user.id

    return redirect ('/dashboard')


@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        return redirect('/')

    user_id = session['user_id']
    user = User.get_by_one({'id': user_id})
    lifts = Lift.get_all()
    return render_template('dashboard.html',user=user,lifts=lifts)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')