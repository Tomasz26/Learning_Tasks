from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class ToWatchForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    done = BooleanField('Have you watched this?')
    submit = SubmitField('Save')