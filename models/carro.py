from main import db

class Carro(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    modelo = db.Column(db.String(50), nullable=False)
    numero_placa = db.Column(db.String(20), nullable=False)
    colaborador = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.modelo
    
    def dicionario(self):
        return {
            'id': self.id,
            'modelo': self.modelo,
            'numero_placa': self.numero_placa,
            'colaborador': self.colaborador
        }