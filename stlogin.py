from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField

class LoginPage(FlaskForm):
    userid=StringField('Username')
    passw=PasswordField('Password')
    submit=SubmitField('Login')
