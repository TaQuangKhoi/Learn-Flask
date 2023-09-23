from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class SignupForm(FlaskForm):
    name = StringField()
    email = StringField()
    password = PasswordField()
    confirm_password = PasswordField()
    submit = SubmitField('Sign Up')
