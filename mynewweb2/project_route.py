import models
from app import db, is_logged_in
from flask import render_template, request, redirect, session
from app import app
from forms import ProjectForm

@app.route('/new_project', methods=['GET', 'POST'])
def new_project():
    form = ProjectForm()
    form.priority.choices = [
        (p.priority_id, p.text) for p in db.session.query(models.Priority).all()
    ]

    form.status.choices = [
        (s.status_id, s.desc) for s in db.session.query(models.Status).all()
    ]

    if is_logged_in():
        user = db.session.query(models.User).filter_by(user_id=session.get('user_id')).first()

        if form.validate_on_submit():
            _description = form.desc.data

            _priority_id = form.priority.data
            _priority = db.session.query(models.Priority).filter_by(priority_id=_priority_id).first()

            _status_id = form.status.data
            _status = db.session.query(models.Status).filter_by(status_id=_status_id).first()

            _project_id = request.form['hiddenProjectId']

            if _project_id == '0':
                project = models.Project(desc=_description, user=user, priority=_priority, status=_status)
                db.session.add(project)

            db.session.commit()
            return redirect('/projects')
        else:
            return render_template('new-project.html', form=form, user=user)
    redirect('/')
