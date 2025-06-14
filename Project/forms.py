from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,FieldList,SelectField,TextAreaField,HiddenField
from wtforms.validators import DataRequired,Length,EqualTo,ValidationError
from Project.models import User

class registeration_form(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(2,30)])
    email=StringField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
    category=FieldList(SelectField("Are you a student or a teacher?",choices=[
        ('student','Student'),
        ('teacher','Teacher'),
    ],validators=[DataRequired()]),min_entries=1)
    submit=SubmitField("Create Account")

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username has already been taken")
    
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email has already been taken")

class login_form(FlaskForm):
    email=StringField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    category=FieldList(SelectField("Are you a student or a teacher?",choices=[
        ('student','Student'),
        ('teacher','Teacher'),
    ],validators=[DataRequired()]),min_entries=1)
    submit=SubmitField("Login")

class project_form(FlaskForm):
    title=StringField("Title",validators=[DataRequired(),Length(2,30)])
    description=TextAreaField("Description",validators=[DataRequired()])
    skills=HiddenField('Add the skills required for this project',validators=[DataRequired()])
    submit=SubmitField("Add Project")