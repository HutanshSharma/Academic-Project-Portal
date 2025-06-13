from Project import db,loginmanager
from flask_login import UserMixin

@loginmanager.user_loader
def user_loader(user_id):
    user=User.query.get(user_id)
    return user

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),unique=True,nullable=False)
    email=db.Column(db.String(30),unique=True,nullable=False)
    password=db.Column(db.String(80),unique=False,nullable=True)
    profile_picture=db.Column(db.String(80),nullable=False,default="default.png")
    role=db.Column(db.String(80),nullable=False)

    def __repr__(self):
        return f"{self.username},{self.email},{self.role}"