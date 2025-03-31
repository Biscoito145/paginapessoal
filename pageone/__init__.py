from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = '23776f32948cb12d7cd472c5f9f52ba8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'peixesapeca145@gmail.com'
app.config['MAIL_PASSWORD'] = 'rjbd vvxh cjnm gont'

database = SQLAlchemy(app)
migrate = Migrate()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'
mail = Mail(app)

migrate.init_app(app, database)

lista_dev = ['Pernalonga', 'Pica-Pau', 'Patolino', 'Scooby-Doo', 'Salsicha']

from pageone import routes