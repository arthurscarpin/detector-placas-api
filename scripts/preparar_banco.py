import json
import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='221100'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)

cursor = conn.cursor()
cursor.execute("DROP DATABASE IF EXISTS `DetectorDePlacas`;")
cursor.execute("CREATE DATABASE `DetectorDePlacas`;")
cursor.execute("USE `DetectorDePlacas`;")

# Criando tabelas
TABLES = {}
TABLES['Usuario'] = ('''
    CREATE TABLE `Usuario` (
        `nome` VARCHAR(50) NOT NULL,
        `sobrenome` VARCHAR(50) NOT NULL,
        `email` VARCHAR(50) NOT NULL,
        `senha` VARCHAR(128) NOT NULL,
        PRIMARY KEY (`email`)      
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Carro'] = ('''
    CREATE TABLE `Carro` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `modelo` VARCHAR(50) NOT NULL,
        `numero_placa` VARCHAR(20) NOT NULL,
        `colaborador` VARCHAR(50) NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}:'.format(tabela_nome), end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')

# Inserindo Usuários
sql = 'INSERT INTO Usuario (nome, sobrenome, email, senha) VALUES (%s, %s, %s, %s)'
usuarios = [
    ('Admin', 'BD', 'admin@email.com', generate_password_hash('admin')),
    ('Arthur', 'Scarpin', 'arthur.carvalho@nc7i.com.br', generate_password_hash('admin')),
    ('Maria', 'Blanco', 'maria@email.com', generate_password_hash('123456')),
    ('João', 'Silva', 'joao.silva@email.com', generate_password_hash('senha123')),
    ('Ana', 'Souza', 'ana.souza@email.com', generate_password_hash('senha456')),
    ('Carlos', 'Pereira', 'carlos.pereira@email.com', generate_password_hash('senha789')),
    ('Beatriz', 'Oliveira', 'beatriz.oliveira@email.com', generate_password_hash('senha101112')),
]
cursor.executemany(sql, usuarios)

print()

cursor.execute('SELECT * FROM Usuario;')
print(' -------------  Usuários:  -------------')
print(f'{"Nome".ljust(10)} | {"Sobrenome".ljust(10)} | {"E-mail".ljust(20)} | {"Senha"}')
for usuario in cursor.fetchall():
    print(f'{usuario[0].ljust(10)} | {usuario[1].ljust(10)} | {usuario[2].ljust(20)} | {usuario[3]}')

# Inserindo Carros
sql = 'INSERT INTO Carro (modelo, numero_placa, colaborador) VALUES (%s, %s, %s)'
carros = [
    ('Honda Civic', 'ABC1D234', 'Pedro'),
    ('Golf GTI', 'ABC2D345', 'Yuri'),
    ('Fox', 'ABC3D456', 'Maria'),
    ('Fiat Uno', 'DEF4G567', 'João'),
    ('Chevrolet Tracker', 'GHI5H678', 'Ana'),
    ('Volkswagen T-Cross', 'JKL6M789', 'Carlos'),
    ('Toyota Corolla', 'MNO7P890', 'Beatriz'),
    ('Nissan Kicks', 'QRS8T901', 'Pedro'),
]
cursor.executemany(sql, carros)

print()

cursor.execute('SELECT * FROM Carro;')
print(' -------------  Veículos:  -------------')
print(f'{"Modelo".ljust(10)} | {"Nº Placa".ljust(10)} | {"Funcionário"}')
for veiculo in cursor.fetchall(): 
    print(f'{veiculo[1].ljust(10)} | {veiculo[2].ljust(10)} | {veiculo[3]}')

# Commitando se não nada tem efeito
conn.commit()
cursor.close()
conn.close()
