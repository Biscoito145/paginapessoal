from pageone.models import Usuario, Post
from pageone import app, database
from pageone import bcrypt
with app.app_context():
    # database.drop_all()
    database.create_all()
    # database.create_all()
    #
    # senha_crip = bcrypt.generate_password_hash('201b94231cba640a1c21').decode('utf-8')
    # usuario1 = Usuario(username='admin123',email='c555f1aee2d56f910c4a0abf22f59ee2@noob.com', senha =senha_crip)
    # usuario2 = Usuario(username='ana1945',email='4566636d29d0b366d14a555309b48d9e@noob.com', senha =senha_crip)
    # usuario3 = Usuario(username='master69',email='0a2004d0b5364fce4ea773cb7413ae34@noob.com', senha =senha_crip)
    # usuario4 = Usuario(username='root777',email='1066efd6377b0829f8bf32765f585524@noob.com', senha =senha_crip)
    # usuario5 = Usuario(username='user00',email='cshudsh17362626337y7fegycbdbeh2uh@noob.com', senha =senha_crip)
    # database.session.add(usuario1)
    # database.session.add(usuario2)
    # database.session.add(usuario3)
    # database.session.add(usuario4)
    # database.session.add(usuario5)
    # database.session.commit()








