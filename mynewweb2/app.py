from flask import Flask, url_for, flash
from forms import SignupForm, LoginForm, TaskForm
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
from models import *


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html', is_logged_in=is_logged_in())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect('/userhome')

    form = LoginForm()
    error = None
    if not form.validate_on_submit():
        return render_template('login.html', form=form)
    # List of all data in request
    _email = form.email.data
    _password = form.password.data

    # Check exist email
    user = db.session.query(models.User).filter_by(email=_email).first()

    if user is None:
        flash(f'Email {_email} does not exist')
    elif user.check_password(_password):
        session['user_id'] = user.user_id
        return render_template('userhome.html', user=user)
    else:
        flash('Password is incorrect')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')


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
        _first_name = form.first_name.data
        _last_name = form.last_name.data
        _email = form.email.data
        _password = form.password.data

        if db.session.query(models.User).filter_by(email=_email).count() == 0:
            new_user = models.User(
                first_name=_first_name,
                last_name=_last_name,
                email=_email,
            )

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


def is_logged_in():
    return session.get('user_id') is not None


from task_routes import *

from project_route import *

with app.test_request_context():
    print(url_for('static', filename='style.css'))

if __name__ == '__main__':
    app.run()
