from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import Email, DataRequired
from flask_wtf.file import FileField, FileRequired


class RegistrationForm(FlaskForm):
    username = StringField("Enter Your Username",validators=[DataRequired()])
    email = EmailField("Enter Your Email", validators=[DataRequired(), Email()])
    bio = StringField("About You", validators=[DataRequired()])
    profile_pic = FileField("Upload Profile Picture")
    cover_pic = FileField("Upload Cover Picture")
    password = PasswordField("Enter Your Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])

    signup = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Enter Your Email", validators=[DataRequired(), Email()])
    password = PasswordField("Enter Your Password", validators=[DataRequired()])
    login = SubmitField('login')