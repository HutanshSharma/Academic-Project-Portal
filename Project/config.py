from dotenv import load_dotenv
import os

load_dotenv()

class config:
    SECRET_KEY="75c26da91c5c7eb2"
    SQLALCHEMY_DATABASE_URI="sqlite:///user.db"
    SQLALCHEMY_TRACK_MODIFICATION=False
    MAIL_SERVER="smtp.gmail.com"
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.getenv("USERMAIL")
    MAIL_PASSWORD=os.getenv("PASSWORD")