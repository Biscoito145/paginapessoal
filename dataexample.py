from pageone.models import Usuario, Post
from pageone import app, database
from pageone import bcrypt
with app.app_context():
    database.drop_all()









