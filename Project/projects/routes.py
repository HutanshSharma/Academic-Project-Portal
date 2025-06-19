import os
from Project import db
from flask import render_template,flash,redirect,request,url_for,abort,Blueprint,current_app
from Project.projects.forms import project_form,submit_project,evaluate_project
from Project.models import Project,Project_Taken,Submission,Evaluation
from flask_login import current_user,login_required
from Project.projects.utils import save_file


projects=Blueprint("projects",__name__)


@projects.route("/project/add",methods=['GET','POST'])
@login_required
def add_project():
    if current_user.role=='student':
        abort(403)
    form=project_form()
    if form.validate_on_submit():
        filename=""
        if form.file_pdf.data:
            filename=save_file(form.file_pdf.data)
        else:
            filename="No pdf"
        post=Project(title=form.title.data,
                     description=form.description.data,
                     skills=form.skills.data,
                     user=current_user,
                     descriptive_pdf=filename)
        current_user.total_projects+=1
        db.session.add(post)
        db.session.commit()
        flash("A new project has been added","success")
        return redirect(url_for("users.profile"))
    elif form.errors:
        flash("Could not add the project","danger")
    return render_template("project_edit.html",form=form,legend="Add New Project")


@projects.route("/project/update/<int:project_id>",methods=['GET','POST'])
@login_required
def update_project(project_id):
    if current_user.role=='student':
        abort(403)
    form=project_form()
    project=Project.query.get(project_id)
    project_name=project.title.strip()
    src=request.args.get("act")
    if form.validate_on_submit():
        if form.file_pdf.data:
            file_name=save_file(form.file_pdf.data)
            if project.descriptive_pdf!="No pdf":
                path=os.path.join(current_app.root_path,'static/project_details',project.descriptive_pdf)
                if os.path.exists(path):
                    os.remove(path)
            project.descriptive_pdf=file_name
            db.session.commit()
        if form.title.data!=project.title or form.description.data!=project.description or form.skills.data!=project.skills:
            project.title=form.title.data
            project.description=form.description.data
            project.skills=form.skills.data
            db.session.commit()
        flash(f"\"{project_name}\" has been updated successfully","success")
        if src:
            return redirect(url_for("projects.more_info"))
        else:
            return redirect(url_for("users.profile"))   
    elif request.method=='GET':
        form.title.data=project.title
        form.description.data=project.description
        form.skills.data=project.skills
    elif form.errors:
        flash(f"\"{project_name}\" could not be updated","danger")
    return render_template("project_edit.html",form=form,legend="Update Project",id="update")


@projects.route("/project/delete/<int:project_id>",methods=['GET','POST'])
@login_required
def delete_project(project_id):
    if current_user.role=='student':
        abort(403)
    project=Project.query.get(project_id)
    project.user.total_projects-=1
    if project.evaluation:
        project.user.total_projects_evaluated-=len(project.evaluation)
        for i in project.evaluation:
            i.submission.user.total_projects_evaluated-=1
    if project.submission:
        project.user.total_projects_submitted-=len(project.submission)
        for i in project.submission:
            i.user.total_projects_submitted-=1
    if project.project_taken_by:
        for i in project.project_taken_by:
            i.user.total_projects_taken-=1
    project_name=project.title.strip()
    db.session.delete(project)
    db.session.commit()
    src=request.args.get("act")
    flash(f"\"{project_name}\" has been deleted successfully","success")
    if src:
        return redirect(url_for("projects.more_info"))
    else:
        return redirect(url_for("users.profile"))
    

@projects.route("/project/take/<int:project_id>")
@login_required
def take_proj(project_id):
    if current_user.role=='teacher':
        abort(403)
    project=Project.query.get(project_id)
    if Project_Taken.query.filter_by(project=project,user=current_user).first():
        flash("Project already taken","danger")
        page=request.args.get("page",1,type=int)
        return redirect(url_for("main.home",page=page))
    if Submission.query.filter_by(project=project,user=current_user).first():
        submission=Submission.query.filter_by(project=project,user=current_user).first()
        if not Evaluation.query.filter_by(project=project,submission=submission).first():
            flash("Project has already been submitted once. You can retake the project after it has been evaluated.","danger")
            page=request.args.get("page",1,type=int)
            return redirect(url_for("main.home",page=page))
    project_taken=Project_Taken(project=project,user=current_user)
    current_user.total_projects_taken+=1
    project.user_count+=1
    db.session.add(project_taken)
    db.session.commit()
    flash("The Project was taken","success")
    page=request.args.get("page",1,type=int)
    return redirect(url_for("main.home",page=page))


@projects.route("/project/student/remove/<int:project_taken_id>",methods=['GET','POST'])
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
    flash(f"\"{project_name}\" has been removed","success")
    src=request.args.get('act')
    if src:
        return redirect(url_for("projects.more_info_taken"))
    else:
        return redirect(url_for("users.profile"))


@projects.route("/project/student/submit/<int:project_taken_id>",methods=['GET','POST'])
@login_required
def submit_proj_taken(project_taken_id):
    if current_user.role=='teacher':
        abort(403)
    project_taken=Project_Taken.query.get(project_taken_id)
    form=submit_project()
    src=request.args.get("act")
    if form.validate_on_submit():
        submit=Submission(info=form.info.data,
                          submission_link=form.project_link.data,
                          user=current_user,
                          project=project_taken.project
                          )
        teacher_name=project_taken.project.user.username.strip()
        project_taken.user.total_projects_taken-=1
        project_taken.user.total_projects_submitted+=1
        project_taken.project.user.total_projects_submitted+=1
        project_taken.project.user_count-=1
        db.session.delete(project_taken)
        db.session.add(submit)
        db.session.commit()
        flash(f"The project has been submitted successfully to \"{teacher_name}\"","success")
        if src:
            return redirect(url_for("projects.more_info_taken"))
        else:
            return redirect(url_for("users.profile"))
    elif form.errors:
        flash("Project could not be submitted","danger")
        print(form.errors)
    return render_template("project_submit.html",form=form,legend="Submit Project")


@projects.route("/project/details/<int:project_id>",methods=['GET','POST'])
def project_details(project_id):
    project=Project.query.get(project_id)
    img_src=url_for("static",filename="/profile_pics/"+project.user.profile_picture)
    pdf=url_for("static",filename="/project_details/"+project.descriptive_pdf)
    return render_template("project_details.html",user=project.user,img_src=img_src,project=project,pdf=pdf)


@projects.route("/project/evaluate/<int:id>")
@login_required
def evaluate(id):
    submission=Submission.query.get(id)
    img_src=url_for("static",filename="/profile_pics/"+submission.user.profile_picture)
    pdf=url_for("static",filename="/project_details/"+submission.project.descriptive_pdf)
    return render_template("evaluate.html",submission=submission,pdf=pdf,img_src=img_src)


@projects.route("/project/evaluate/form/<int:id>",methods=["GET","POST"])
@login_required
def evaluate_form(id):
    form=evaluate_project()
    submission=Submission.query.get(id)
    src=request.args.get("act")
    if form.validate_on_submit():
        evaluation=Evaluation(score=form.score.data/10,
                              feedback=form.feedback.data,
                              submission=submission,
                              user=current_user,
                              project=submission.project
                              )
        current_user.total_projects_evaluated+=1
        submission.user.total_projects_evaluated+=1
        db.session.add(evaluation)
        db.session.commit()
        flash("You reviews have been submitted","success")
        if src:
            return redirect(url_for("projects.more_info_submission"))
        else:
            return redirect(url_for("users.profile"))
    return render_template("evaluate_form.html",legend="Reviews",form=form)


@projects.route("/project/reviews/<int:id>")
@login_required
def reviews(id):
    evaluation=Evaluation.query.get(id)
    submission=evaluation.submission
    img_src=url_for("static",filename="/profile_pics/"+evaluation.user.profile_picture)
    pdf=url_for("static",filename="/project_details/"+submission.project.descriptive_pdf)
    return render_template("reviews.html",evaluation=evaluation,submission=submission,img_src=img_src,pdf=pdf)


@projects.route("/profile/moreinfo/projects")
@login_required
def more_info():
    projects=current_user.project
    projects.reverse()
    return render_template("more-info/more_projects.html",projects=projects,title="Projects")


@projects.route("/profile/moreinfo/submission")
@login_required
def more_info_submission():
    projects=current_user.project
    submissions=[]
    for i in projects:
        submission=Submission.query.filter_by(project=i).all()
        submissions.extend(submission)
    submissions.reverse()
    return render_template("more-info/more-submission.html",submissions=submissions)


@projects.route("/profile/moreinfo/evaluation")
@login_required
def more_info_evaluation():
    evaluation=current_user.evaluation
    evaluation.reverse()
    return render_template("more-info/more-evaluation.html",evaluation=evaluation)


@projects.route("/profile/moreinfo/taken")
@login_required
def more_info_taken():
    projects=current_user.project_taken
    projects.reverse()
    return render_template("more-info/more-taken.html",projects=projects)


@projects.route("/profile/moreinfo/submitted")
@login_required
def more_info_submitted():
    submissions=current_user.submission
    submissions.reverse()
    return render_template("more-info/more-submitted.html",submissions=submissions)