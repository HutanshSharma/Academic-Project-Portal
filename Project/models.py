from Project import db,loginmanager
from flask_login import UserMixin
from datetime import datetime

@loginmanager.user_loader
def user_loader(user_id):
    user=User.query.get(user_id)
    return user

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),unique=True,nullable=False)
    email=db.Column(db.String(30),unique=True,nullable=False)
    password=db.Column(db.String(80),unique=False,nullable=False)
    total_projects=db.Column(db.Integer,nullable=False,default=0)
    total_projects_taken=db.Column(db.Integer,nullable=False,default=0)
    total_projects_submitted=db.Column(db.Integer,nullable=False,default=0)
    total_projects_evaluated=db.Column(db.Integer,nullable=False,default=0)
    profile_picture=db.Column(db.String(80),nullable=False,default="default.png")
    role=db.Column(db.String(80),nullable=False)
    project=db.relationship("Project",backref="user",lazy=True,cascade="all,delete")
    submission=db.relationship("Submission",backref="user",lazy=True,cascade="all,delete")
    evaluation=db.relationship("Evaluation",backref="user",lazy=True,cascade="all,delete")
    project_taken=db.relationship("Project_Taken",backref="user",lazy=True,cascade="all,delete")

    def __repr__(self):
        return f"{self.username},{self.email},{self.role}"
    
class Project(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    description=db.Column(db.Text,nullable=False)
    skills=db.Column(db.Text,nullable=False)
    descriptive_pdf=db.Column(db.String(80),nullable=False,default='No pdf')
    user_count=db.Column(db.Integer,nullable=False,default=0)
    created_at=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    created_by=db.Column(db.Integer,db.ForeignKey('user.id'))
    submission=db.relationship('Submission',backref='project',lazy=True,cascade="all,delete")
    project_taken_by=db.relationship('Project_Taken',backref='project',lazy=True,cascade="all,delete")

    def __repr__(self):
        return f"{self.title},{self.created_at},{self.created_by}"
    
class Submission(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    submitted_at=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    submission_link=db.Column(db.Text,nullable=False)
    info=db.Column(db.Text)
    project_id=db.Column(db.Integer,db.ForeignKey('project.id'),unique=True)
    student_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    evaluation=db.relationship('Evaluation',backref='submission',lazy=True,cascade="all,delete")

    def __repr__(self):
        return f"{self.submission_link}"
    
class Evaluation(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    score=db.Column(db.Integer,nullable=False)
    feedback=db.Column(db.Text,nullable=False)
    evaluated_at=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    submission_id=db.Column(db.Integer,db.ForeignKey('submission.id'),unique=True)
    evaluated_by=db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.score},{self.feedback}"
    
class Project_Taken(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    taken_at=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    project_id=db.Column(db.Integer,db.ForeignKey('project.id'),unique=True)
    student_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.taken_at}"