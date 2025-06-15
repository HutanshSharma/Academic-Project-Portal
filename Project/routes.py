import os
import secrets
from PIL import Image
from Project import app,db,bcrypt
from flask import render_template,flash,redirect,request,url_for,abort
from Project.forms import registeration_form,login_form,project_form,update_profile_form
from Project.models import User,Project,Project_Taken
from flask_login import login_user,current_user,login_required,logout_user


@app.route("/")
@app.route("/home")
def home():
    projects=Project.query.all()
    return render_template("home.html",title="Home",projects=projects)


@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
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
        return redirect(url_for('login'))
    return render_template("register.html",form=form,title="Register")


@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form=login_form()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data) and user.role==form.category.data[0]:
                login_user(user,remember=False)
                flash("You have been logged in successfully","success")
                return redirect(url_for("home"))
            else:
                flash("Login unsuccessful check your details","danger")
        else:
                flash("User doesn't exists","danger")
                return redirect(url_for("register"))
    return render_template("login.html",title="Login",form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/profile")
@login_required
def profile():
    img_src=url_for("static",filename="/profile_pics/"+current_user.profile_picture)
    if current_user.role=='teacher':
        projects=current_user.project
        return render_template("profile_teacher.html",title=current_user.username,img_src=img_src,projects=projects)
    elif current_user.role=='student':
        projects=current_user.project_taken
        return render_template("profile_student.html",title=current_user.username,img_src=img_src,projects=projects)

def save_pic(picture):
    hex_name=secrets.token_hex(8)
    _,extension=os.path.splitext(picture.filename)
    file_name=hex_name+extension
    path=os.path.join(app.root_path,'static/profile_pics',file_name)
    size=(125,125)
    i=Image.open(picture)
    i.thumbnail(size)
    i.save(path)
    return file_name


@app.route("/profile/update",methods=["GET","POST"])
@login_required
def update_profile():
    form=update_profile_form()
    if form.validate_on_submit():
        if form.image.data:
            file_name=save_pic(form.image.data)
            current_user.profile_picture=file_name
            db.session.commit()
        if current_user.username!=form.username.data or current_user.email!=form.email.data:
            current_user.username=form.username.data
            current_user.email=form.email.data
            db.session.commit()
        flash("Changes made","success")
        return redirect(url_for("profile"))
    elif request.method=="GET":
        form.username.data=current_user.username
        form.email.data=current_user.email
    return render_template("update_profile.html",title=current_user.username,form=form)


def save_file(fname):
    fname_hex=secrets.token_hex(8)
    _,fext=os.path.splitext(fname.filename)
    fname_new=fname_hex+fext
    path=os.path.join(app.root_path,'static/project_details',fname_new)
    fname.save(path)
    return fname_new


@app.route("/project/add",methods=['GET','POST'])
@login_required
def add_project():
    if current_user.role=='student':
        abort(403)
    form=project_form()
    if form.validate_on_submit():
        filename=save_file(form.file_pdf.data)
        post=Project(title=form.title.data,
                     description=form.description.data,
                     skills=form.skills.data,
                     user=current_user,
                     descriptive_pdf=filename)
        current_user.total_projects+=1
        db.session.add(post)
        db.session.commit()
        flash("A new project has been added","success")
        return redirect(url_for("profile"))
    elif form.errors:
        flash("Could not add the project","danger")
    return render_template("project_edit.html",title=current_user.username,form=form,legend="Add New Project")


@app.route("/project/update/<int:project_id>",methods=['GET','POST'])
@login_required
def update_project(project_id):
    if current_user.role=='student':
        abort(403)
    form=project_form()
    project=Project.query.get(project_id)
    project_name=project.title.strip()
    if form.validate_on_submit():
        if form.title.data!=project.title or form.description.data!=project.description or form.skills.data!=project.skills:
            project.title=form.title.data
            project.description=form.description.data
            project.skills=form.skills.data
            db.session.commit()
            flash(f"\"{project_name}\" has been updated successfully","success")
            return redirect(url_for("profile"))   
    elif request.method=='GET':
        form.title.data=project.title
        form.description.data=project.description
        form.skills.data=project.skills
    elif form.errors:
        flash(f"\"{project_name}\" could not be updated","danger")
    return render_template("project_edit.html",title=current_user.username,form=form,legend="Update Project",id="update")


@app.route("/project/delete/<int:project_id>",methods=['GET','POST'])
@login_required
def delete_project(project_id):
    if current_user.role=='student':
        abort(403)
    project=Project.query.get(project_id)
    project.user.total_projects-=1
    project_name=project.title.strip()
    db.session.delete(project)
    db.session.commit()
    flash(f"\"{project_name}\" has been deleted successfully","success")
    return redirect(url_for("profile"))
    

@app.route("/project/take/<int:project_id>")
@login_required
def take_proj(project_id):
    if current_user.role=='teacher':
        abort(403)
    project=Project.query.get(project_id)
    if Project_Taken.query.filter_by(project=project,user=current_user).first():
        flash("Project already taken","danger")
        return redirect(url_for("home"))
    project_taken=Project_Taken(project=project,user=current_user)
    current_user.total_projects_taken+=1
    project.user_count+=1
    db.session.add(project_taken)
    db.session.commit()
    flash("The Project was taken","success")
    return redirect(url_for("home"))


@app.route("/project/student/remove/<int:project_taken_id>",methods=['GET','POST'])
@login_required
def remove_proj_taken(project_taken_id):
    if current_user.role=='teacher':
        abort(403)
    project_taken=Project_Taken.query.get(project_taken_id)
    project_taken.project.user_count-=1
    project_taken.user.total_projects_taken-=1
    project_name=project_taken.project.title.strip()
    db.session.delete(project_taken)
    db.session.commit()
    flash(f"\"{project_name}\"has been removed","success")
    return redirect(url_for("profile"))


@app.route("/project/student/submit/<int:project_taken_id>",methods=['GET','POST'])
@login_required
def submit_proj_taken(project_taken_id):
    project_taken=Project_Taken.query.get(project_taken_id)
    return render_template("project_submit.html",title=current_user.username)


@app.route("/project/details/<int:project_id>",methods=['GET','POST'])
@login_required
def project_details(project_id):
    project=Project.query.get(project_id)
    return render_template("project_details.html",title=project.title)
