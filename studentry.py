from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField,TextAreaField

class StudentEntry(FlaskForm):
   stid=IntegerField('StudentID')
   stdname=StringField('StudentName')
   phone=IntegerField('phone')
   secclass=StringField('Class')
   father=StringField('FatherName')
   mother=StringField('MotherName')
   address=TextAreaField('Address')
   submit=SubmitField('Submit')
	
	