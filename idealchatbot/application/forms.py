from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional
)

class SignupForm(FlaskForm):
    """User Sign-up Form."""
    fullname = StringField(
        'Name',
        validators=[
            Length(min=1, max=100),
            DataRequired()]
    )
    outlet = StringField(
        'Outlet',
        validators=[
            Length(min=7, max=7)
        ]
    )
    number = PasswordField(
        'Number',
        validators=[
            DataRequired(),
            Length(min=11, max=11, message="That's not a number")
        ]
    )
    confirm = PasswordField(
        'Confirm Your Number',
        validators=[
            DataRequired(),
            EqualTo('number', message='Numbers must match.')
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    outlet = StringField(
        'Outlet',
        validators=[
            DataRequired(),
            Length(min=7, max=7, message="That's not a valid Outlet Code")
        ]
    )
    number = PasswordField('Number', validators=[DataRequired()])
    submit = SubmitField('Log In')