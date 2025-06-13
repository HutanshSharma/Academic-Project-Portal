from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask(__name__)

app.config['SECRET_KEY']="75c26da91c5c7eb2"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
loginmanager=LoginManager(app)

from Project import routes