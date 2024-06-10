from database import db
class Remitente(db.Model):
    __tablename__ = 'Remitente'
    id = db.Column(db.Integer, primary_key=True)
    rut_remitente = db.Column(db.String(10), db.ForeignKey('Cliente.rut'), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'rut_remitente': self.rut_remitente,
            'direccion': self.direccion,
            'correo': self.correo
        }
