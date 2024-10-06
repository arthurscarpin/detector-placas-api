from main import app, db
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from models.carro import Carro

@app.route('/carros', methods=['GET'])
@jwt_required()
def carros():
    '''
    Rota que permite que o usuário consulte todos os carros cadastrados.
    '''
    lista_carros = Carro.query.order_by(Carro.id).all()
    return jsonify([carro.dicionario() for carro in lista_carros]), 200

@app.route('/carros/<int:id>', methods=['GET'])
@jwt_required()
def carro_por_id(id):
    '''
    Rota que permite que o usuário consulte um carro já cadastrado pelo <id>.
    '''
    carro = Carro.query.get(id)
    if carro:
        return jsonify(carro.dicionario()), 200 
    else:
        return jsonify({"mensagem": "Carro não encontrado!"}), 404

@app.route('/cadastrar-carro', methods=['POST'])
@jwt_required()
def cadastrar_carro():
    '''
    Rota que permite que o usuário cadastre um novo carro.
    '''
    dados = request.get_json()
    modelo = dados.get('modelo').strip().title()
    placa = dados.get('numero_placa').strip().upper()
    colaborador = dados.get('colaborador').strip().title()
    
    carro_duplicado= Carro.query.filter_by(numero_placa=placa).first()

    if carro_duplicado:
        return jsonify({'mensagem': 'A placa já possui cadastro.'}), 400  
      
    novo_carro = Carro(modelo=modelo, numero_placa=placa, colaborador=colaborador) 
    db.session.add(novo_carro)
    db.session.commit()   
    return jsonify(novo_carro.dicionario()), 201

@app.route('/editar-carro/<int:id>', methods=['PUT'])
@jwt_required()
def editar_carro(id):
    '''
    Rota que permite que o usuário altere um carro já cadastrado através do <id>.
    '''
    dados = request.get_json()
    modelo = dados.get('modelo').strip()
    colaborador = dados.get('colaborador').strip()

    carro = Carro.query.get(id)
    if not carro:
        return jsonify({'mensagem': 'Carro não encontrado.'}), 404

    carro.modelo = modelo
    carro.colaborador = colaborador
    db.session.commit()
    return jsonify(carro.dicionario()), 200

@app.route('/deletar-carro/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_carro(id):
    '''
    Rota que permite que o usuário deletar um carro pelo <id>.
    '''
    carro = Carro.query.get(id)
    if carro:
        db.session.delete(carro)
        db.session.commit()
        return jsonify({"mensagem": "Carro deletado com sucesso!"}), 200 
    else:
        return jsonify({"mensagem": "Carro não encontrado!"}), 404
    
@app.route('/status/<string:numero_placa>', methods=['POST'])
@jwt_required()
def verificar_status_carro(numero_placa):
    '''
    Rota que verifica o status do veículo
    '''
    placa = numero_placa.upper()
    carro = Carro.query.filter_by(numero_placa=placa).first()

    if not carro:
        return jsonify({'status': 'Veículon não autorizado!'}), 404

    return jsonify({'status': 'Veículo autorizado!'}), 200