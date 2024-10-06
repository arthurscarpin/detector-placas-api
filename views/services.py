import os
import cv2
import easyocr
from main import app, smtp_server, smtp_email, smtp_senha, smtp_port
from main import app
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from datetime import datetime
from services.imagem_ocr import ImagemOCR
from models.usuario import Usuario
from services.email import Email

@app.route('/email', methods=['POST'])
def enviar_email():
    '''
    Rota para resetar senha via e-mail
    '''
    dados = request.get_json()

    email = dados.get('email').strip()
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({'mensagem': 'Email não encontrado!'}), 404

    envio = Email(smtp_server, smtp_port, smtp_email, smtp_senha, email)
    envio.enviar_email()
    return jsonify({'mensagem': envio.enviar_email()}), 200

@app.route('/upload-arquivo', methods=['POST'])
@jwt_required()
def upload_arquivo():
    '''
    Rota que permite o usuário realizar o upload da imagem e retorna a placa detectada.
    '''
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo foi enviado"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    data_hora_atual = datetime.now()
    data_hora_formatada = data_hora_atual.strftime("%d%m%Y_%H%M%S")
    os.makedirs('content', exist_ok=True)
    caminho_arquivo = os.path.join('content', f'placa_{data_hora_formatada}.png')
    file.save(caminho_arquivo)

    imagem = cv2.imread(caminho_arquivo)
    leitor = easyocr.Reader(lang_list=['pt'], gpu=True)
    ocr = ImagemOCR(imagem, leitor)
    resultado_ocr = ocr.executar_ocr_imagem()

    return jsonify({"numero_placa": resultado_ocr}), 200
