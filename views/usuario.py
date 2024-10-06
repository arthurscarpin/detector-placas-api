from main import app, db
from flask import jsonify, request, redirect
from flask_jwt_extended import create_access_token, jwt_required
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required
from models.usuario import Usuario

@app.route('/')
def index():
    '''
    Rota principal que é redirecionada para a rota autenticar
    '''
    return redirect('/autenticar')

@app.route('/autenticar', methods=['POST'])
def autenticar_endpoint():
    '''
    Rota que permite que os usuários se autentiquem usando suas credenciais (email e senha).
    '''
    dados = request.get_json()

    if not dados or 'email' not in dados or 'senha' not in dados:
        return jsonify({'mensagem': 'Dados insuficientes!'}), 400

    email = dados.get('email').strip().lower()
    senha = dados.get('senha').strip() 
    usuario_db = Usuario.query.filter_by(email=email).first()

    if usuario_db and check_password_hash(usuario_db.senha, senha):
        token = create_access_token(identity=email)
        
        return jsonify(
            access_token=token,
            nome=usuario_db.nome,
            sobrenome=usuario_db.sobrenome
        ), 200
    
    return jsonify({'codigo': 401, 'mensagem': 'Login incorreto!'}), 401

@app.route('/cadastrar-usuario', methods=['POST'])
def cadastrar_usuario():
    '''
    Rota que permite cadastrar um novo usuário.
    '''
    dados = request.get_json()
    nome = dados.get('nome').strip().title()
    sobrenome = dados.get('sobrenome').strip().title()
    email = dados.get('email').strip().lower()
    senha = dados.get('senha').strip()

    usuario_duplicado = Usuario.query.filter_by(email=email).first()
    
    if usuario_duplicado:
        return jsonify({'mensagem': 'O usuário já possoi cadastro!'}), 400
    
    senha_hash = generate_password_hash(senha)

    novo_usuario = Usuario(nome=nome, sobrenome=sobrenome, email=email, senha=senha_hash)
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify(novo_usuario.dicionario()), 201

@app.route('/editar-usuario/<string:email>', methods=['PUT'])
@jwt_required()
def editar_usuario(email):
    '''
    Rota que permite que o usuário edite as suas informações pessoais pelo <email>.
    '''
    dados = request.get_json()

    nome = dados.get('nome').strip().title()
    sobrenome = dados.get('sobrenome').strip().title()
    senha = dados.get('senha').strip()

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado.'}), 404

    usuario.nome = nome
    usuario.sobrenome = sobrenome
    usuario.senha = generate_password_hash(senha)
    db.session.commit()
    return jsonify(usuario.dicionario()), 200

@app.route('/deletar-usuario/<string:email>', methods=['DELETE'])
@jwt_required()
def deletar_usuario(email):
    '''
    Rota que permite que o usuário deletar um usuario carro pelo <email>.
    '''
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"mensagem": "Usuário deletado com sucesso!"}), 200 
    else:
        return jsonify({"mensagem": "Usuário não encontrado!"}), 404