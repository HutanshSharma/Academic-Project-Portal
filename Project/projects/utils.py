import secrets
import os
from flask import current_app


def save_file(fname):
    fname_hex=secrets.token_hex(8)
    _,fext=os.path.splitext(fname.filename)
    fname_new=fname_hex+fext
    path=os.path.join(current_app.root_path,'static/project_details',fname_new)
    fname.save(path)
    return fname_new

