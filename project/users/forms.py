#Imports related to forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

#Imports related to users
from flask_login import current_user
from project.models import User

class RegistrationForm(FlaskForm):

    mobile = StringField("Mobile number", validators = [DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("passConfirm", message="Passwords don't match!")])
    passConfirm = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Sign up")

class LoginForm(FlaskForm):

    mobile = StringField("Mobile number", validators = [DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")

class AddStockForm(FlaskForm):

    sticker = StringField("Stock sticker", validators = [DataRequired()])
    submit = SubmitField("Add stock")
