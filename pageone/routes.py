from flask import render_template, request, redirect, url_for, flash, abort
from pageone.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, FormContato
from pageone import app, lista_dev, database, bcrypt, mail
from pageone.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image
from flask_mail import  Message


@app.route("/")
def home():
    posts = Post.query.order_by(Post.id.desc())

    return render_template('home.html', posts=posts)

@app.route('/contato', methods=['POST', 'GET'])
def contato():
    form = FormContato()
    if form.validate_on_submit():
        email = form.email.data
        men = form.mensagem.data
        nome = form.nome.data
        msg = Message('Novo Contato via site', recipients=['peixesapeca@usp.br'], sender='peixesapeca145@gmail.com')
        msg.body = f'Mensagem: {men}\nEnviado por {nome} ({email})'
        mail.send(msg)
        flash("Mensagem Enviada com sucesso!", 'alert-success')

    return render_template('contato.html', form=form)

@app.route('/desenvolvedores')
def dev():
    lista_devs = Usuario.query.all()
    return render_template('dev.html', lista_devs=lista_devs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        user = Usuario.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(str(user.senha), form_login.senha.data):
            login_user(user, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no email: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return(redirect(par_next))
            else:
                return redirect(url_for('home'))
        # login realizado com sucesso
        else:
            flash(f'Falha no Login. Email ou Senha Incorretos', 'alert-danger')

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_crip = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
        user = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_crip)
        with app.app_context():
            database.session.add(user)
            database.session.commit()

        flash(f'Conta criada com sucesso no email: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

def salvar_file(imagem):
    # adicionar um codigo na imagem
    codigo = secrets.token_hex(8)
    if imagem.filename[-4] == '.':
        extensao = imagem.filename[-4:]
        nome = imagem.filename[:-4]
    else:
        extensao = imagem.filename[-5:]
        nome = imagem.filename[:-5]
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/files', nome_arquivo)

    return caminho_completo, nome_arquivo

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        if form.file.data:
            # pego o nome do arquivo
            #salvo o arquivo
            caminho, nome_arquivo = salvar_file(form.file.data)
            form.file.data.save(caminho)

            post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user, file=nome_arquivo)
        else:
            post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html',foto_perfil=foto_perfil)


def salvar_imagem(imagem):
    # adicionar um codigo na imagem
    codigo = secrets.token_hex(8)
    extensao = imagem.filename[-4:]
    nome = imagem.filename[:-4]
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (200,200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


    # redimensionar a imagem
    # salvar a iamgem
    pass

@app.route('/editarperfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()

    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data

        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        database.session.commit()
        flash('Perfil Alterdado com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
def ver_post(post_id):
    print(f"post_id: {post_id}")
    post = Post.query.get(post_id)

    if post is None:
        print(f"Post com ID {post_id} não encontrado!")
        flash('Post não encontrado', 'alert-danger')
        return redirect(url_for('home'))

    print(f"Post encontrado: {post.id}")

    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
            form.file.data = post.file
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            if form.file.data:
                caminho, nome_arquivo = salvar_file(form.file.data)
                post.file = nome_arquivo
                form.file.data.save(caminho)
            database.session.commit()
            flash('Post Editado Com Sucesso!', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None

    return render_template('verpost.html', post=post, form=form)


@app.route('/post/<post_id>/excluir' , methods=['POST', 'GET'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash("Post Excluído Com Sucesso", 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)