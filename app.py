from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from models import Usuario
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-virtual-life-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app)

lm = LoginManager(app)
lm.login_view = 'login'

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

    nome = request.form["nomeForm"]
    senha = request.form["senhaForm"]

    usuario = db.session.query(Usuario).filter_by(nome=nome).first()

    if not usuario or not check_password_hash(usuario.senha, senha):
        return render_template('login.html', erro="Nome ou senha incorretos.")

    login_user(usuario)
    return redirect(url_for('home'))

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registrar.html')

    nome = request.form["nomeForm"]
    senha = request.form["senhaForm"]

    if db.session.query(Usuario).filter_by(nome=nome).first():
        return render_template('registrar.html', erro="Nome de usuário já existe.")

    novo_usuario = Usuario(nome=nome, senha=generate_password_hash(senha))
    db.session.add(novo_usuario)
    db.session.commit()
    
    login_user(novo_usuario)
    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('inicial'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)