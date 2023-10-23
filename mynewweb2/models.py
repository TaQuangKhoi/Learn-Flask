from app import db
from sqlalchemy import Sequence
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    user_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=True)
    last_name = db.Column(db.String(64), index=True, nullable=True)
    email = db.Column(db.String(64), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(64), index=True, nullable=False)

    projects = db.relationship('Project', back_populates='user')

    def __repr__(self):
        return f'<User ({self.first_name}, {self.last_name}, {self.email}, {self.password_hash})>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        return self.password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Status(db.Model):
    status_id = db.Column(db.Integer, Sequence('status_id_seq'), primary_key=True)
    desc = db.Column(db.String(64), nullable=False)

    projects = db.relationship('Project', back_populates='status')
    tasks = db.relationship('Task', back_populates='status')

    def __repr__(self):
        return f'<Status {self.status_id} with text {self.text}>'


class Task(db.Model):
    task_id = db.Column(db.Integer, Sequence('task_id_seq'), primary_key=True)
    description = db.Column(db.String(128), nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'))
    project = db.relationship('Project', back_populates='tasks')

    priority_id = db.Column(db.Integer, db.ForeignKey('priority.priority_id'))
    priority = db.relationship('Priority', back_populates='tasks')

    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'))
    status = db.relationship('Status', back_populates='tasks')

    deadline = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Task ({self.description}, {self.user_id})>'

    def get_priority_class(self):
        if self.priority_id == 1:
            return 'table-danger'
        elif self.priority_id == 2:
            return 'table-warning'
        elif self.priority_id == 3:
            return 'table-info'
        else:
            return 'table-primary'


class Priority(db.Model):
    priority_id = db.Column(db.Integer, Sequence('priority_id_seq'), primary_key=True)
    text = db.Column(db.String(64), nullable=True)
    desc = db.Column(db.String(64), nullable=True)

    tasks = db.relationship('Task', back_populates='priority')

    def __repr__(self):
        return f'<Priority {self.priority_id} with text {self.text}>'


class Project(db.Model):
    project_id = db.Column(db.Integer, Sequence('project_id_seq'), primary_key=True)

    name = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.String(128), nullable=False)
    deadline = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship('User', back_populates='projects')

    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'))
    status = db.relationship('Status', back_populates='projects')

    tasks = db.relationship('Task', back_populates='project')

    def __repr__(self):
        return f'<Project {self.project_id} with name {self.name}>'
