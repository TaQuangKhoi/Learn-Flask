from flask import Flask, url_for, request, render_template, flash, session, redirect
from forms import SignupForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

baseDir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'haovan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

import models


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


def do_the_login(req):
    # data from form
    # username = req.form['username']
    # print(username)
    # password = req.form['password']
    # print(password)
    return 'Done'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        # List of all data in request
        _email = form.email.data
        _password = form.password.data

        # Check exist email
        user = db.session.query(models.User).filter_by(email=_email).first()

        if user is None:
            flash(f'Email {_email} does not exist')
        else:
            # Check password
            if user.check_password(_password):
                session['user_id'] = user.user_id
                return render_template('userhome.html', user=user)
            else:
                flash(f'Password is incorrect')

        return do_the_login(request)
    else:
        return render_template('login.html', form=form)


@app.get('/signup')
def signup_get():
    form = SignupForm()
    return render_template('signup.html', form=form)


@app.post('/signup')
def signup_post():
    form = SignupForm()
    print(form.data)
    if form.validate_on_submit():
        print('Form validated')
        _name = form.name.data
        _email = form.email.data
        _password = form.password.data
        print(_name, _email, _password)

        if db.session.query(models.User).filter_by(email=_email).count() == 0:
            new_user = models.User(full_name=_name, email=_email)
            new_user.set_password(_password)
            db.session.add(new_user)
            db.session.commit()

            return render_template('sign-up-succeed.html', user=new_user)
        else:
            flash(f'Email {_email} already exists')
            return render_template('signup.html', form=form)

    print(form.errors)

    print('Form not validated')
    return render_template('signup.html', form=form)


@app.route('/userhome', methods=['GET', 'POST'])
def userHome():
    print("session: ", session)
    _user_id = session.get('user_id')
    print("_user_id: ", _user_id)

    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        return render_template('userhome.html', user=user)
    else:
        return redirect('/login')
        # return "Test"


with app.test_request_context():
    print(url_for('static', filename='style.css'))

if __name__ == '__main__':
    app.run()
