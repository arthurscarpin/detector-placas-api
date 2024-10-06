from main import db

class Usuario(db.Model):
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), primary_key=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.nome
    
    def dicionario(self):
        return {
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'email': self.email
        }