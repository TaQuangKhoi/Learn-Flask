import models
from app import db, is_logged_in
from flask import render_template, request, redirect, session
from app import app
from forms import ProjectForm


@app.route('/projects', methods=['GET', 'POST'])
def projects_list():
    if not is_logged_in():
        return redirect('/login')

    _user_id = session.get('user_id')

    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        return render_template('projects.html', user=user, is_logged_in=is_logged_in())
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
                    name = _name,
                    deadline = _deadline,
                    desc=_description, user=user, status=_status
                )
                db.session.add(project)

            db.session.commit()
            return redirect('/projects')
        else:
            return render_template('new-project.html', form=form, user=user)
    redirect('/')
