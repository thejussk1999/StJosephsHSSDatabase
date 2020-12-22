from flask_wtf import FlaskForm
from wtforms import IntegerField,SubmitField,StringField

class UpdateMarks(FlaskForm):
   stid=IntegerField('Student ID')
   subid=StringField('Subject ID')
   marks=IntegerField('Marks')
   submit=SubmitField('Update')