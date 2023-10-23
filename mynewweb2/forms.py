from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo


class SignupForm(FlaskForm):
    name = StringField('Name')

    first_name = StringField('First Name', validators=[DataRequired(
        message='Please enter your first name'
    )])

    last_name = StringField('Last Name', validators=[DataRequired(
        message='Please enter your last name'
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
        EqualTo('confirm_password', message='Passwords must match')
    ])
    terms = BooleanField('I agree all statements in <a href="#!">Terms of service</a>')

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
    priority = SelectField('Priority', coerce = int)

    submitAdd = SubmitField('Add Task')
    submitUpdate = SubmitField('Update Task')


class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(
            message='Please enter a name'
        ),
    ])
    desc = StringField('Description', validators=[
        DataRequired(
            message='Please enter a description'
        ),
    ])
    deadline = DateField('Deadline', validators=[
        DataRequired(
            message='Please choose a deadline'
        ),
    ])
    priority = SelectField('Priority', coerce = int)
    status = SelectField('Status', coerce = int)

    submitAdd = SubmitField('Add Project')
    submitUpdate = SubmitField('Update Project')