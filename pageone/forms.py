from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from pageone.models import Usuario
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

class FormCriarConta(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirma_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Esse e-mail já está cadastrado. Use outro para continuar')


class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')

class FormContato(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mensagem = StringField('Informe sua mensagem aqui', validators=[DataRequired()])
    botao_submit_enviar = SubmitField('Enviar Mensagem')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'gif', 'mp4'])])
    botao_submit_editar = SubmitField('Confirmar Edição')

    def validate_email(selfs, email):
        if current_user.email != email.data:
            user = Usuario.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Esse e-mail já está cadastrado. Use outro email')

class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2,1500)])
    corpo = TextAreaField('Texto do Post', validators=[DataRequired()])
    file = FileField('Colocar Anexo', validators=[FileAllowed(['jpg', 'png', 'gif', 'mp4', 'pdf', 'xlsx', 'mp3', 'txt', 'exe', 'pptx','pptm', 'ppsx', 'mov', 'avi', 'jpeg'])])
    botao_submit_criar = SubmitField('Criar Post')


