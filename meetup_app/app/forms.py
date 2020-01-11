from flask import flash, redirect
from flask_wtf import RecaptchaField, Recaptcha, FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=64, message="`Username must be between 4 and 64 characters long.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128, message="`Password must be between 8 and 128 characters long.")])
    remember = BooleanField('Remember Me')


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=64, message="`Email must be less than 64 characters.")])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=64, message="`Username must be between 4 and 64 characters long.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128, message="`Password must be between 8 and 128 characters long.")])
    password2 = PasswordField('Retype Password', validators=[DataRequired(), EqualTo('password', message="`Passwords must match")])
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Recaptcha must be completed")])

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first() is not None:
            raise ValidationError('`Username taken')
            return redirect('/')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first() is not None:
            raise ValidationError('`That email is already associated with a MeetUp account.')
            return redirect('/')


class EventForm(FlaskForm):
    eventName = StringField('eventName', validators=[InputRequired(), Length(max=32, message='-Event names must not exceed 32 characters.')])
    dates = HiddenField('dates', validators=[InputRequired(message='-You must select at least one day for your event.')])
    startTime = StringField('startTime', validators=[InputRequired(message='-You must select an earliest start time.')])
    endTime = StringField('endTime', validators=[InputRequired(message='-You must select a latest end time.')])
    eventName = StringField('eventName', validators=[InputRequired(), Length(max=32, message='`Event names must not exceed 32 characters.')])
    dates = HiddenField('dates', validators=[InputRequired()])
    startTime = StringField('startTime', validators=[InputRequired()])
    endTime = StringField('endTime', validators=[InputRequired()])


class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('`There is no account with that email.')
            redirect('/')


class ScheduleForm(FlaskForm):
    user_name = StringField('Your Name', validators=[InputRequired(), Length(max=64, message='-Name must not exceed 64 characters.')])
    availability = HiddenField('availability', validators=[DataRequired()])

    def validate_name(self, user_name):
        if User.query.filter_by(username=user_name.data).first() is not None:
            raise ValidationError('-Cannot use that name')
            redirect('/')


class PScheduleForm(FlaskForm):
    pAvailability = HiddenField('pAvailability', validators=[DataRequired()])


class InviteToEventForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit = SubmitField('Invite to Event')
    
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


