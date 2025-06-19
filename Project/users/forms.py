from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,FieldList,SelectField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import DataRequired,Length,EqualTo,ValidationError,Email
from Project.models import User
from flask_login import current_user


class registeration_form(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(2,30)])
    email=StringField("Email",validators=[DataRequired(),Email()])
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


class update_profile_form(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(2,30)])
    email=StringField("Email",validators=[DataRequired()])
    image=FileField("Profile picture",validators=[FileAllowed(['png','jpg','jpeg'])])
    submit=SubmitField("Update Profile")


    def validate_username(self,username):
        if username.data!=current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This username has already been taken")
    
    def validate_email(self,email):
        if email.data!=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email has already been taken")
            

class reset_password_email_form(FlaskForm):
    email=StringField("Email",validators=[DataRequired()])
    submit=SubmitField("Send Email")


class reset_password_form(FlaskForm):
    password=PasswordField("Password",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField("Reset Password")
