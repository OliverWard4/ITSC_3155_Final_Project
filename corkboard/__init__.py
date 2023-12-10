import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from docx import Document
from io import BytesIO
from pdf2image import convert_from_path

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'richcomo123@gmail.com'  # Use your actual environment variable name
app.config['MAIL_PASSWORD'] = 'ttka qvas cldz ltvg'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mail = Mail(app)

# Update the file_type function
# Update the file_type function
def file_type(filename):
    _, extension = os.path.splitext(filename)
    if extension.lower() in ('.jpg', '.jpeg', '.png', '.gif'):
        return 'image'
    elif extension.lower() in ('.mp4', '.avi', '.mkv'):
        return 'video'
    elif extension.lower() == '.pdf':
        return 'pdf'
    elif extension.lower() == '.docx':
        return 'docx'
    else:
        return 'other'



# Add the file_type filter to the Jinja environment
app.jinja_env.filters['file_type'] = file_type

