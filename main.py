import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('settings/config.py')

CORS(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

smtp_config = app.config['SMTP']
smtp_server = smtp_config['smtp_server']
smtp_port = smtp_config['smtp_port']
smtp_email = smtp_config['smtp_email']
smtp_senha = smtp_config['smtp_senha']

os.makedirs(app.config['CONTENT_FOLDER'], exist_ok=True)

from views.usuario import *
from views.carro import *
from views.services import *

if __name__ == '__main__':
    app.run(debug=True)
