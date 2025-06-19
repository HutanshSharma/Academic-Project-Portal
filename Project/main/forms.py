from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FieldList,SelectField
from wtforms.validators import DataRequired


class search_projects(FlaskForm):
    category=FieldList(SelectField("Search By",choices=[
        ('teacher_name','Teacher name'),
        ('project_name','Project name'),
        ('skill','Skill')
    ],validators=[DataRequired()]),min_entries=1)
    search=StringField("Search here",validators=[DataRequired()])
    submit=SubmitField("Search")