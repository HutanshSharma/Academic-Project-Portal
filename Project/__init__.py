from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from Project.config import config
from flask_mail import Mail

db=SQLAlchemy()
bcrypt=Bcrypt()
loginmanager=LoginManager()
mail=Mail()

def create_app(current_config=config):
    app=Flask(__name__)
    app.config.from_object(config)

    from Project.users.routes import users
    from Project.projects.routes import projects
    from Project.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(projects)
    app.register_blueprint(main)

    db.init_app(app)
    bcrypt.init_app(app)
    loginmanager.init_app(app)
    mail.init_app(app)
    
    return app