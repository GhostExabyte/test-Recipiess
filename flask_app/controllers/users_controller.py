
from flask_app import app
from flask import render_template, request, redirect, flash, session

from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User

bcrypt=Bcrypt(app)

@app.route('/')
def display_login():
    return render_template('login.html')
    
@app.route('/user/registration', methods =['POST'] )
def process_registration():
    if User.validate_registration(request.form) == False:
        return redirect('/')
    user_exists = User.get_one_to_validate_email (request.form)
    if user_exists != None:
        flash('Baka! This email already exists!','error_registration_email')
        return redirect('/')
        
    data = {
        **request.form,
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    
    user_id = User.create(data)

    session['first_name'] = data ['first_name']
    session['email'] = data['email']
    session['user_id'] = user_id

    return redirect('/recipes')

@app.route("/user/login", methods = ['POST'])
def process_login():
    current_user = User.get_one_to_validate_email(request.form)
    if not bcrypt.check_password_hash (current_user.password,request.form["password"] ):
        flash('Wrong credentials','error_login_credentials')
        return redirect('/')
    
    

    session['first_name'] = current_user.first_name
    session['email'] = current_user.email
    session['user_id'] = current_user.id

    return redirect('/recipes')

@app.route('/user/logout')
def process_logout():
    session.clear()
    return redirect('/')

