from flask_wtf import FlaskForm
from wtforms import IntegerField,SubmitField

class StudentLog(FlaskForm):
   stid=IntegerField('Student ID')
   submit=SubmitField('Login')
	