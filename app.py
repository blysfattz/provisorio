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
        return render_template('registrar.html',
                               nome_digitado=nome,
                               **erros)

    novo_usuario = Usuario(nome=nome, senha=generate_password_hash(senha))
    db.session.add(novo_usuario)
    db.session.commit()
    login_user(novo_usuario)
    return redirect(url_for("home"))
