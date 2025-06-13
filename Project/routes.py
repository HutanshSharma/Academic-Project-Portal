from Project import app,db,bcrypt
from flask import render_template,flash,redirect,request,url_for
from Project.forms import registeration_form,login_form
from Project.models import User
from flask_login import login_user,current_user,login_required,logout_user

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",title="Home")

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
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=False)
            flash("You have been logged in","success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful","danger")
    return render_template("login.html",title="Login",form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html",title=current_user.username)