from app import db
from sqlalchemy import Sequence


class User(db.Model):
    user_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(64), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(64), index=True, nullable=False)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name} {self.email} {self.password_hash}>'