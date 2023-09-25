from flask import Flask, url_for, request, render_template
from forms import SignupForm
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


def show_the_login_form():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # List of all data in request
        print(request.values.keys())

        return do_the_login(request)
    else:
        return show_the_login_form()


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

        new_user = models.User(full_name=_name, email=_email)
        new_user.set_password(_password)
        db.session.add(new_user)
        db.session.commit()

        return render_template('sign-up-succeed.html', user=new_user)

    print(form.errors)

    print('Form not validated')
    return render_template('signup.html', form=form)


with app.test_request_context():
    print(url_for('static', filename='style.css'))

if __name__ == '__main__':
    app.run()
