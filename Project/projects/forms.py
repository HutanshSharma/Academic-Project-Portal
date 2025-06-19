from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,HiddenField,IntegerRangeField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import DataRequired,Length


class project_form(FlaskForm):
    title=StringField("Title",validators=[DataRequired(),Length(2,100)])
    description=TextAreaField("Description",validators=[DataRequired()])
    skills=HiddenField('Add the skills required for this project',validators=[DataRequired()])
    file_pdf=FileField("Upload the pdf with the project details",validators=[FileAllowed(['pdf','txt'])])
    submit=SubmitField("Submit")

      
class submit_project(FlaskForm):
    info=TextAreaField("Briefly Describe your submission",validators=[DataRequired()])
    project_link=StringField("Enter the link to you Repository",validators=[DataRequired()])
    submit=SubmitField("Submit Project")


class evaluate_project(FlaskForm):
    score=IntegerRangeField("Rate this project (1-10)",default=0,validators=[DataRequired()])
    feedback=TextAreaField("Give feedback here",validators=[DataRequired()])
    submit=SubmitField("Submit Reviews")    
