from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired


class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(
        message='Please enter your name'
    )])
    email = StringField('Email', validators=[
        DataRequired(
            message='Please enter your email'
        ),
        Email(
            message='Please enter a valid email'
        )
    ])
    password = PasswordField('Password', validators=[
        DataRequired(
            message='Please enter a password'
        ),
        EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Sign Up')
