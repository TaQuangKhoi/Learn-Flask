import models
from app import db, is_logged_in
from flask import render_template, request, redirect, session, flash
from app import app
from forms import *
from datetime import datetime, timedelta


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


@app.route('/new_task/<projectId>', methods=['GET', 'POST'])
def new_task_by_project(projectId):
    form = TaskForm()

    form.priority.choices = [
        (p.priority_id, p.desc) for p in db.session.query(models.Priority).all()
    ]

    form.status.choices = [
        (s.status_id, s.desc) for s in db.session.query(models.Status).all()
    ]

    if is_logged_in():
        user = db.session.query(models.User).filter_by(user_id=session.get('user_id')).first()

        project = db.session.query(models.Project).filter_by(project_id=projectId).first()

        if form.deadline.data:
            print('form Deadline', form.deadline.data, type(form.deadline.data))
            print('project Deadline', project.deadline, type(project.deadline))
            if form.deadline.data > project.deadline:
                print('Deadline is invalid')
                # flash(f'Deadline must be before {project.deadline}')
            else:
                print('Deadline is valid')

        if form.validate_on_submit():
            _description = form.description.data

            _priority_id = form.priority.data
            _priority = db.session.query(models.Priority).filter_by(priority_id=_priority_id).first()

            _status_id = form.status.data
            _status = db.session.query(models.Status).filter_by(status_id=_status_id).first()

            _task_id = request.form['hiddenTaskId']

            _deadline = form.deadline.data

            if _task_id == '0':
                task = models.Task(
                    description=_description, project=project, priority=_priority, status=_status,
                    deadline=_deadline
                )
                db.session.add(task)

            db.session.commit()
            check_if_all_tasks_in_projects_completed(projectId)
            return redirect('/project_detail/' + projectId)
        else:
            return render_template('new-task.html', form=form, user=user, project=project)
    redirect('/')


@app.route('/deleteTask', methods=['GET', 'POST'])
def delete_task():
    _user_id = session.get('user_id')
    if _user_id:
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
            print("task: ", task)
            db.session.delete(task)
            db.session.commit()

        return redirect('/userhome')

    return redirect('/login')


@app.route('/delete_task/<projectId>', methods=['GET', 'POST'])
def delete_task_redirect_to_project(projectId):
    _user_id = session.get('user_id')
    if _user_id:
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
            db.session.delete(task)
            db.session.commit()

        return redirect('/project_detail/' + projectId)

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


@app.route('/edit_task/<projectId>', methods=['GET', 'POST'])
def edit_task_by_project(projectId):
    form = TaskForm()

    form.priority.choices = [
        (p.priority_id, p.desc) for p in db.session.query(models.Priority).all()
    ]

    form.status.choices = [
        (s.status_id, s.desc) for s in db.session.query(models.Status).all()
    ]

    _user_id = session.get('user_id')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        _task_id = request.form['hiddenTaskId']
        project = db.session.query(models.Project).filter_by(project_id=projectId).first()
        if _task_id:
            if form.submitUpdate.data:
                print('Update task', form.data)
                _description = form.description.data

                _priority_id = form.priority.data
                _priority = db.session.query(models.Priority).filter_by(priority_id=_priority_id).first()

                _status_id = form.status.data
                _status = db.session.query(models.Status).filter_by(status_id=_status_id).first()

                if _status.desc == 'Đang thực hiện':
                    update_project_status(projectId, _status_id)

                _deadline = form.deadline.data

                task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
                task.description = _description
                task.priority = _priority
                task.status = _status
                task.deadline = _deadline

                db.session.commit()
                check_if_all_tasks_in_projects_completed(projectId)
                return redirect('/project_detail/' + projectId)
            else:
                task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
                form.process()
                form.description.data = task.description
                form.priority.data = task.priority.priority_id
                form.status.data = task.status.status_id
                form.deadline.data = task.deadline
                check_if_all_tasks_in_projects_completed(projectId)
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


def update_project_status(project_id, status_id):
    project = db.session.query(models.Project).filter_by(project_id=project_id).first()
    project.status_id = status_id
    db.session.commit()


def check_if_all_tasks_in_projects_completed(project_id):
    tasks = db.session.query(models.Task).filter_by(project_id=project_id).all()
    count = 0
    for task in tasks:
        if task.status.desc == 'Hoàn thành':
            count += 1
    if count == len(tasks):
        update_project_status(project_id, 4)
    else:
        update_project_status(project_id, 2)
