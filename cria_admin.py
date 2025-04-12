from  pageone import bcrypt, app, database
from pageone.models import Usuario

with app.app_context():
    database.create_all()
    senha_crip = bcrypt.generate_password_hash('201b94231cba640a1c21').decode('utf-8')
    usuario1 = Usuario(username='admin123',email='c555f1aee2d56f910c4a0abf22f59ee2@noob.com', senha =senha_crip)
    database.session.add(usuario1)
    database.session.commit()
    print("Usuario Criado com Sucesso")