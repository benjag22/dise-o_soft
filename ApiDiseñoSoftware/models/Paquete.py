from database import db
class Paquete(db.Model):
    __tablename__ = 'Paquete'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    peso = db.Column(db.Numeric, nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False)

    __table_args__ = (
        db.CheckConstraint("tipo IN ('sobre', 'encomienda')"),
        db.CheckConstraint("peso >= 0.0"),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'peso': str(self.peso),  # Convertir a string para evitar problemas con JSON
            'fecha_ingreso': self.fecha_ingreso.isoformat()  # Convertir a string ISO
        }
