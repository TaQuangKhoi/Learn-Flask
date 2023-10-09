from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(
        message='Please enter your name'
    )])
    email = StringField('Email', validators=[
        Email(
            message='Please enter a valid email'
        ),
        DataRequired(
            message='Please enter your email'
        ),
    ])
    password = PasswordField('Password', validators=[
        DataRequired(
            message='Please enter a password'
        ),
        # EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        Email(
            message='Please enter a valid email'
        ),
        DataRequired(
            message='Please enter your email'
        ),
    ])
    password = PasswordField('Password', validators=[
        DataRequired(
            message='Please enter a password'
        ),
    ])
    submit = SubmitField('Login')


class TaskForm(FlaskForm):
    description = StringField('Description', validators=[
        DataRequired(
            message='Please enter a description'
        ),
    ])
    submit = SubmitField('Add Task')

