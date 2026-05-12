from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from models import Usuario
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-virtual-life-2026')
lm = LoginManager(app)
lm.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

@lm.user_loader
def user_loader(id):
    return db.session.get(Usuario, int(id))  

@app.route('/')
def inicial():
    return render_template('inicio.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    nome  = request.form.get("nomeForm", "").strip()
    senha = request.form.get("senhaForm", "")
    user  = db.session.query(Usuario).filter_by(nome=nome).first()
    if not user or not check_password_hash(user.senha, senha):
        return render_template('login.html', erro='Nome ou senha incorretos.')
    login_user(user)  
    return redirect(url_for('home'))

@app.route('/registrar', methods=['POST', 'GET'])
def registrar():
    if request.method == "GET":
        return render_template('registrar.html')
    nome     = request.form.get("nomeForm", "").strip()
    senha    = request.form.get("senhaForm", "")
    confirma = request.form.get("confirmaForm", "")
    erros    = {}
    if not nome:
        erros['erro_nome'] = 'O nome é obrigatório.'
    elif db.session.query(Usuario).filter_by(nome=nome).first():
        erros['erro_nome'] = 'Este nome de usuário já está em uso.'
    if not senha:
        erros['erro_senha'] = 'A senha é obrigatória.'
    elif len(senha) < 6:
        erros['erro_senha'] = 'A senha deve ter no mínimo 6 caracteres.'
    if senha and confirma and senha != confirma:
        erros['erro_confirma'] = 'As senhas não coincidem.'
    if erros:
        return render_template('registrar.html', nome_digitado=nome, **erros)
    novo_usuario = Usuario(nome=nome, senha=generate_password_hash(senha))
    db.session.add(novo_usuario)
    db.session.commit()
    login_user(novo_usuario)
    return redirect(url_for("home"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('inicial'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
