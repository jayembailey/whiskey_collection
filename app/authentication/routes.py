from forms import UserSignupForm, UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['POST', 'GET'])
def signup():
    form = UserSignupForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data

            print(f'signup try: {email}, {password}')
            
            user = User(email, first_name, last_name, password)
            print(f' before add: {user.email}')
            db.session.add(user)
            print(f' before commit: {user.first_name} {user.last_name}')
            db.session.commit()

            flash(f'User {email} successfully created.')
            return redirect(url_for('site.home'))
    
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_up.html', form = form)

@auth.route('/signin', methods = ['POST', 'GET'])
def signin():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('Successful login. Good job!', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('No dice. Try again.', 'auth-fail')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid data: Check your credentials')
    return(render_template('sign_in.html', form = form))

@auth.route('/logout', methods = ['POST', 'GET'])
def logout():
    logout_user()
    flash('You are now logged out.')
    return redirect(url_for('site.home'))