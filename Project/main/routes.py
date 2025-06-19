from flask import render_template,request,Blueprint
from Project.main.forms import search_projects
from Project.models import User,Project


main=Blueprint("main",__name__)


@main.route("/")
@main.route("/home",methods=['GET','POST'])
def home():
    page=request.args.get('page',1,type=int)
    form=search_projects()
    if form.validate_on_submit():
        if form.category.data[0]=='teacher_name':
            projects=Project.query.filter(Project.user.has(User.username==form.search.data)).order_by(Project.created_at.desc()).all()
            return render_template("home.html",projects=projects,form=form)
        elif form.category.data[0]=='project_name':
            projects=Project.query.filter_by(title=form.search.data).all()
            return render_template("home.html",projects=projects,form=form)
        elif form.category.data[0]=='skill':
            skill=form.search.data
            list=Project.query.order_by(Project.created_at.desc()).all()
            projects=[]
            for i in list:
                if skill in i.skills:
                    projects.append(i)
            return render_template("home.html",projects=projects,form=form)
    projects=Project.query.order_by(Project.created_at.desc()).paginate(page=page,max_per_page=6)
    return render_template("home.html",projects=projects,page=page,form=form)

