from app import db
from sqlalchemy import Sequence
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    user_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    #full_name = db.Column(db.String(128), index=True, nullable=False)
    first_name = db.Column(db.String(64), index=True, nullable=True)
    last_name = db.Column(db.String(64), index=True, nullable=True)
    email = db.Column(db.String(64), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(64), index=True, nullable=False)

    tasks = db.relationship('Task', back_populates='user')

    def __repr__(self):
        return f'<User ({self.first_name}, {self.last_name}, {self.email}, {self.password_hash})>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        return self.password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    task_id = db.Column(db.Integer, Sequence('task_id_seq'), primary_key=True)
    description = db.Column(db.String(128), nullable=False)
    isCompleted = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship('User', back_populates='tasks')

    priority_id = db.Column(db.Integer, db.ForeignKey('priority.priority_id'))
    priority = db.relationship('Priority', back_populates='tasks')

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
    text = db.Column(db.String(64), nullable=False)

    tasks = db.relationship('Task', back_populates='priority')

    def __repr__(self):
        return f'<Priority {self.priority_id} with text {self.text}>'


