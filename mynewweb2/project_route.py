import models
from app import db, is_logged_in
from flask import render_template, request, redirect, session
from app import app
from forms import *


@app.route('/projects', methods=['GET', 'POST'])
def projects_list():
    if not is_logged_in():
        return redirect('/login')

    _user_id = session.get('user_id')

    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        form = SearchProjectForm()
        return render_template('projects.html', user=user, projects=user.projects, form=form,
                               is_logged_in=is_logged_in())
    else:
        return redirect('/login')


@app.route('/new_project', methods=['GET', 'POST'])
def new_project():
    form = ProjectForm()

    form.status.choices = [
        (s.status_id, s.desc) for s in db.session.query(models.Status).all()
    ]

    if is_logged_in():
        user = db.session.query(models.User).filter_by(user_id=session.get('user_id')).first()

        if form.validate_on_submit():
            _name = form.name.data

            _description = form.desc.data

            _deadline = form.deadline.data

            _status_id = form.status.data
            _status = db.session.query(models.Status).filter_by(status_id=_status_id).first()

            _project_id = request.form['hiddenProjectId']

            if _project_id == '0':
                project = models.Project(
                    name=_name,
                    deadline=_deadline,
                    desc=_description, user=user, status=_status
                )
                db.session.add(project)

            db.session.commit()
            return redirect('/projects')
        else:
            return render_template('new-project.html', form=form, user=user)
    redirect('/')


@app.route('/delete_project', methods=['GET', 'POST'])
def delete_project():
    _user_id = session.get('user_id')
    if _user_id:
        _project_id = request.form['hiddenProjectId']
        if _project_id:
            project = db.session.query(models.Project).filter_by(project_id=_project_id).first()
            db.session.delete(project)
            db.session.commit()

        return redirect('/projects')

    return redirect('/login')


@app.route('/edit_project', methods=['GET', 'POST'])
def edit_project():
    form = ProjectForm()

    form.status.choices = [
        (s.status_id, s.desc) for s in db.session.query(models.Status).all()
    ]

    _user_id = session.get('user_id')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        _project_id = request.form['hiddenProjectId']
        print("_project_id: " + _project_id)
        if _project_id:
            if form.submitUpdate.data:
                print('Update project', form.data)
                _name = form.name.data

                _description = form.desc.data

                _deadline = form.deadline.data

                _status_id = form.status.data
                _status = db.session.query(models.Status).filter_by(status_id=_status_id).first()

                project = db.session.query(models.Project).filter_by(project_id=_project_id).first()

                project.name = _name
                project.desc = _description
                project.deadline = _deadline
                project.status = _status

                db.session.commit()
                return redirect('/projects')
            else:
                project = db.session.query(models.Project).filter_by(project_id=_project_id).first()
                form.process()

                form.name.data = project.name
                form.desc.data = project.desc
                form.deadline.data = project.deadline
                form.status.data = project.status.status_id

                return render_template('new-project.html', form=form, user=user, project=project)
        elif form.validate_on_submit():
            print('Form validated')

    return redirect('/')


@app.route('/project_detail/<projectId>', methods=['GET'])
def project_detail(projectId):
    _user_id = session.get('user_id')
    if not _user_id:
        return redirect('/login')

    user = db.session.query(models.User).filter_by(user_id=_user_id).first()
    project = db.session.query(models.Project).filter_by(project_id=projectId).first()

    form = SearchTaskForm()

    return render_template(
        'project_detail.html',
        user=user,
        project=project,
        form=form,
        tasks=project.tasks,
        is_logged_in=is_logged_in(),
    )


@app.route('/search_project', methods=['GET', 'POST'])
def search_project():
    _user_id = session.get('user_id')
    if not _user_id:
        return redirect('/login')

    form = SearchProjectForm()
    user = db.session.query(models.User).filter_by(user_id=_user_id).first()
    keyword = form.keyword.data

    form.keyword.data = keyword

    projects = db.session.query(models.Project).filter(models.Project.name.like('%' + keyword + '%')).all()
    for project in projects:
        print(project)
    print(keyword)
    return render_template(
        'projects.html',
        user=user,
        projects=projects,
        form=form,
        is_logged_in=is_logged_in()
    )


@app.route('/search_tasks', methods=['GET', 'POST'])
def search_tasks():
    _user_id = session.get('user_id')
    if not _user_id:
        return redirect('/login')

    project_id = request.form['hiddenProjectIdForSearch']
    project = db.session.query(models.Project).filter_by(project_id=project_id).first()

    form = SearchProjectForm()
    user = db.session.query(models.User).filter_by(user_id=_user_id).first()
    keyword = form.keyword.data

    form.keyword.data = keyword
    # filter in project with id is project_id
    tasks = db.session.query(models.Task).filter(models.Task.project_id == project_id).filter(
        models.Task.description.like('%' + keyword + '%')).all()
    return render_template(
        'project_detail.html',
        user=user,
        tasks=tasks,
        form=form,
        project=project,
        is_logged_in=is_logged_in()
    )
