import secrets
import os
from PIL import Image
from flask import current_app,url_for
from flask_mail import Message
from Project import mail


def save_pic(picture):
    hex_name=secrets.token_hex(8)
    _,extension=os.path.splitext(picture.filename)
    file_name=hex_name+extension
    path=os.path.join(current_app.root_path,'static/profile_pics',file_name)
    size=(125,125)
    i=Image.open(picture)
    i.thumbnail(size)
    i.save(path)
    return file_name


def send_mail(user):
    token=user.create_token()
    msg=Message("Password Reset Request",sender="hutanshsharma241005@gmail.com",recipients=[user.email])
    msg.body=f"""To reset you password go to the following link
{url_for('users.reset_password',token=token,_external=True)}
"""
    mail.send(msg)

