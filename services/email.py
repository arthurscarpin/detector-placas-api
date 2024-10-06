import os
import string
import random
import smtplib
import logging
from flask_bcrypt import generate_password_hash
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from models.usuario import Usuario
from main import db

class Email():
    def __init__(self, smtp_server, smtp_port, email_smtp, senha_smtp, email_reset):
        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port
        self.__email_smtp = email_smtp
        self.__senha_smtp = senha_smtp
        self.__email_reset = email_reset

    def enviar_email(self):
        usuario = Usuario.query.filter_by(email=self.__email_reset).first()

        if usuario is not None:
            nova_senha = 'A123456'
            usuario.senha = generate_password_hash(nova_senha)
            db.session.commit()

            try:
                titulo = '[Access Control] - Recuperação de senha'
                mensagem = f'''
                <html>
                    <body>
                        <p>Olá,</p>
                        <p>Recebemos uma solicitação para a recuperação da sua senha. Sua nova senha é: {nova_senha}</p>
                        <p>Por motivos de segurança, recomendamos que você altere essa senha assim que fizer login na sua conta.</p>
                        <p>Atenciosamente,</p>
                        <strong>Suporte AccessControl</strong>
                        <p><img src="cid:logo" alt="AccessControl Logo" style="width:100px;"/></p>
                    </body>
                </html>
                '''

                msg = MIMEMultipart()
                msg['From'] = self.__email_smtp
                msg['To'] = self.__email_reset
                msg['Subject'] = titulo
                msg.attach(MIMEText(mensagem, 'html'))

                path = os.path.join(os.path.dirname(__file__), '..', 'content', 'logo', 'guarda.png')
                if not os.path.exists(path):
                    return f'Arquivo de imagem não encontrado: {path}'

                with open(path, 'rb') as f:
                    logo = MIMEImage(f.read())
                    logo.add_header('Content-ID', '<logo>')
                    msg.attach(logo)
                
                server = smtplib.SMTP(self.__smtp_server, self.__smtp_port)
                server.starttls()
                server.login(self.__email_smtp, self.__senha_smtp)
                server.sendmail(self.__email_smtp, self.__email_reset, msg.as_string())
                server.quit()
                
                return f'A nova senha foi enviada para o e-mail: {self.__email_reset}'
            except Exception as error:
                logging.error(f'Erro ao enviar o e-mail: {str(error)}')
                return f'Erro ao enviar o e-mail: {str(error)}'
        else:
            return f'O e-mail {self.__email_reset} não possui cadastro!'
