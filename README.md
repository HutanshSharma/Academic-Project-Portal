
# Teacher-Student-Project-App

A robust web-based platform designed for streamlined project collaboration between **teachers** and **students**. Teachers can create and manage academic projects, while students can take up projects, submit work, and receive evaluations.

---

## Features

### For Teachers:
- Secure registration and login
- Add, edit, delete project listings
- View student submissions
- Evaluate submitted work with feedback

### For Students:
- Register/login with student role
- Browse and search projects by title, teacher, or skill
- Take up and submit projects
- View evaluations and feedback

### General:
- Full authentication system using `Flask-Login`
- Role-based access control
- SQLite database with SQLAlchemy ORM
- Secure file upload for project PDFs
- Upload and preview profile pictures
- Pagination and "load more" features
- Forgot password functionality via email (Flask-Mail) with time-sensitive reset tokens
- Blueprint-based modular Flask app structure
- Custom error pages (404, 403, 500)

---

## Tech Stack

| Category       | Technologies Used                                |
|----------------|--------------------------------------------------|
| **Backend**    | Flask, SQLAlchemy, Flask-Login, Flask-WTF        |
| **Frontend**   | HTML, CSS, Bootstrap, JavaScript                 |
| **Database**   | SQLite                                            |
| **ORM**        | SQLAlchemy                                        |
| **Email**      | Flask-Mail (for password reset functionality)    |
| **File Handling** | Python `os`, `secrets`, Pillow (PIL)            |
| **Authentication** | Flask-Login, Bcrypt for password hashing      |

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Teacher-Student-Project-Manager.git
cd Teacher-Student-Project-Manager
```

### 2. Setup a virtual environment if you want

### 3. Download the required packages 

```bash
pip install -r requirements.txt
```

### 4. Setup the database by opening the python interpreter
```bash
from Project import db,create_app
from Project.models import *
app=create_app()
app.app_context().push()
db.create_all()
```

### 5. Setup the environment variables for your email address and password

### 6. Run the app

```bash
python app.py
```
