from database import db
class Destinatario(db.Model):
    __tablename__ = 'Destinatario'
    id = db.Column(db.Integer, primary_key=True)
    rut_destinatario = db.Column(db.String(10), db.ForeignKey('Cliente.rut'), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'rut_destinatario': self.rut_destinatario,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'correo': self.correo
        }
