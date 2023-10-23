from flask import Flask, url_for, request, render_template, flash, session, redirect
from forms import SignupForm, LoginForm, TaskForm, ProjectForm
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
    return render_template('index.html', is_logged_in=is_logged_in())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect('/userhome')

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

        # return do_the_login(request)
    else:
        return render_template('login.html', form=form)


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
                first_name = _first_name,
                last_name = _last_name,
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


@app.route('/userhome', methods=['GET', 'POST'])
def user_home():
    if not is_logged_in():
        return redirect('/login')

    _user_id = session.get('user_id')

    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        return render_template('userhome.html', user=user, is_logged_in=is_logged_in())
    else:
        return redirect('/login')


@app.route('/newTask', methods=['GET', 'POST'])
def new_task():
    form = TaskForm()
    form.priority.choices = [
        (p.priority_id, p.text) for p in db.session.query(models.Priority).all()
    ]

    if is_logged_in():
        user = db.session.query(models.User).filter_by(user_id=session.get('user_id')).first()

        if form.validate_on_submit():
            _description = form.description.data

            _priority_id = form.priority.data
            _priority = db.session.query(models.Priority).filter_by(priority_id=_priority_id).first()

            _task_id = request.form['hiddenTaskId']
            print(_task_id)

            if _task_id == '0':
                task = models.Task(description=_description, user=user, priority=_priority)
                db.session.add(task)

            db.session.commit()
            return redirect('/userhome')
        else:
            return render_template('new-task.html', form=form, user=user)
    redirect('/')


@app.route('/deleteTask', methods=['GET', 'POST'])
def delete_task():
    _user_id = session.get('user_id')
    if _user_id:
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
            db.session.delete(task)
            db.session.commit()

        return redirect('/userhome')

    return redirect('/login')


@app.route('/editTask', methods=['GET', 'POST'])
def edit_task():
    form = TaskForm()
    form.priority.choices = [
        (p.priority_id, p.text) for p in db.session.query(models.Priority).all()
    ]

    _user_id = session.get('user_id')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            if form.submitUpdate.data:
                print('Update task', form.data)
                _description = form.description.data
                _priority_id = form.priority.data
                _priority = db.session.query(models.Priority).filter_by(priority_id=_priority_id).first()

                task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
                task.description = _description
                task.priority = _priority
                db.session.commit()
                return redirect('/userhome')
            else:
                task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
                form.process()
                form.description.data = task.description
                form.priority.data = task.priority.priority_id
                return render_template('new-task.html', form=form, user=user, task=task)
        elif form.validate_on_submit():
            print('Form validated')

    return redirect('/')


@app.route('/doneTask', methods=['GET', 'POST'])
def done_task():
    _user_id = session.get('user_id')
    if _user_id:
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
            task.isCompleted = True
            db.session.commit()

        return redirect('/userhome')

    return redirect('/')


@app.route('/projects', methods=['GET', 'POST'])
def projects_list():
    if not is_logged_in():
        return redirect('/login')

    _user_id = session.get('user_id')

    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        return render_template('userhome.html', user=user, is_logged_in=is_logged_in())
    else:
        return redirect('/login')


import project_route


with app.test_request_context():
    print(url_for('static', filename='style.css'))

if __name__ == '__main__':
    app.run()
