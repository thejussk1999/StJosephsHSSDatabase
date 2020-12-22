from flask_wtf import FlaskForm
from wtforms import IntegerField,SubmitField

class StudentDelete(FlaskForm):
   stid=IntegerField('Student ID')
   submit=SubmitField('Remove')
	
	