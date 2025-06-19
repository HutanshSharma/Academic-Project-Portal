import os
from Project import db,bcrypt
from flask import render_template,flash,redirect,request,url_for,Blueprint
from Project.users.forms import registeration_form,login_form,update_profile_form,reset_password_email_form,reset_password_form
from Project.models import User,Submission
from flask_login import login_user,current_user,login_required,logout_user
from Project.users.utils import save_pic,send_mail

users=Blueprint("users",__name__)

@users.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form=registeration_form()
    if form.validate_on_submit():
        password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,
                  email=form.email.data,
                  password=password,
                  role=form.category.data[0])
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created successfully","success")
        return redirect(url_for('users.login'))
    return render_template("register.html",form=form)


@users.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form=login_form()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data) and user.role==form.category.data[0]:
                login_user(user,remember=False)
                flash("You have been logged in successfully","success")
                return redirect(url_for("main.home"))
            else:
                flash("Login unsuccessful check your details","danger")
        else:
                flash("User doesn't exists","danger")
                return redirect(url_for("users.register"))
    return render_template("login.html",form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/profile")
@login_required
def profile():
    img_src=url_for("static",filename="/profile_pics/"+current_user.profile_picture)
    if current_user.role=='teacher':
        project_loadmore=False
        submission_loadmore=False
        evaluation_loadmore=False
        projects=current_user.project
        if len(projects)>5:
            project_loadmore=True
        submissions=[]
        for i in projects:
            submission=Submission.query.filter_by(project=i).all()
            submissions.extend(submission)
        projects.reverse()
        submissions.reverse()
        if len(submissions)>5:
            submission_loadmore=True
        evaluation=current_user.evaluation
        evaluation.reverse()
        if len(evaluation)>5:
            evaluation_loadmore=True
        return render_template("profile_teacher.html",img_src=img_src,projects=projects[:5],submissions=submissions[:5],
                               evaluation=evaluation[:5],plm=project_loadmore,slm=submission_loadmore,elm=evaluation_loadmore)
    elif current_user.role=='student':
        project_loadmore=False
        submission_loadmore=False
        projects=current_user.project_taken
        projects.reverse()
        if len(projects)>5:
            project_loadmore=True
        submissions=current_user.submission
        submissions.reverse()
        if len(submissions)>5:
            submission_loadmore=True
        return render_template("profile_student.html",img_src=img_src,projects=projects[:5],submissions=submissions[:5],plm=project_loadmore,slm=submission_loadmore)


@users.route("/profile/update",methods=["GET","POST"])
@login_required
def update_profile():
    form=update_profile_form()
    if form.validate_on_submit():
        if form.image.data:
            file_name=save_pic(form.image.data)
            if current_user.profile_picture!="default.png":
                path=os.path.join(users.root_path,'static/profile_pics',current_user.profile_picture)
                if os.path.exists(path):
                    os.remove(path)
            current_user.profile_picture=file_name
            db.session.commit()
        if current_user.username!=form.username.data or current_user.email!=form.email.data:
            current_user.username=form.username.data
            current_user.email=form.email.data
            db.session.commit()
        flash("Changes made","success")
        return redirect(url_for("users.profile"))
    elif request.method=="GET":
        form.username.data=current_user.username
        form.email.data=current_user.email
    return render_template("update_profile.html",form=form)


@users.route("/reset_password_email",methods=['GET','POST'])
def reset_password_email():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form=reset_password_email_form()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            send_mail(user)
        flash('You will recieve an email with the reset password link if the email is registered','info')
        return redirect(url_for("users.login"))
    return render_template("reset_password/reset_password_email.html",form=form)


@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    user_id=User.verify_token(token)
    if user_id is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for("users.reset_password_email"))
    form=reset_password_form()
    if form.validate_on_submit():
        user=User.query.get(user_id['user_id'])
        user.password=bcrypt.generate_password_hash(form.password.data)
        db.session.commit()
        flash("The password has been changed successfully","success")
        return redirect(url_for("users.login"))
    return render_template("reset_password/reset_password.html",form=form)


