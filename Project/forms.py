from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,FieldList,SelectField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo

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

class login_form(FlaskForm):
    email=StringField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    category=FieldList(SelectField("Are you a student or a teacher?",choices=[
        ('student','Student'),
        ('teacher','Teacher'),
    ],validators=[DataRequired()]),min_entries=1)
    submit=SubmitField("Login")