from database import db
class Historial(db.Model):
    __tablename__ = 'Historial'
    id = db.Column(db.Integer, primary_key=True)
    fecha_mod = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    id_envio = db.Column(db.Integer, db.ForeignKey('Envio.id'), nullable=False)

    __table_args__ = (
        db.CheckConstraint("estado IN ('en preparación', 'en tránsito', 'en sucursal', 'en reparto', 'entregado')"),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'fecha_mod': self.fecha_mod.isoformat(),
            'estado': self.estado,
            'id_envio': self.id_envio
        }
