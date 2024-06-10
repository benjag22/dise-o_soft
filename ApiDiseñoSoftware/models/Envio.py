from database import db
class Envio(db.Model):
    __tablename__ = 'Envio'
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(20), nullable=False)
    recogida_a_domicilio = db.Column(db.Boolean, nullable=False)
    por_pagar = db.Column(db.Boolean, nullable=False)
    tipo_envio = db.Column(db.String(20), nullable=False)
    codigo_postal = db.Column(db.String(10), nullable=False)
    fecha_recepcion = db.Column(db.Date, nullable=False)
    reparto_a_domicilio = db.Column(db.Date, nullable=True)
    pagado = db.Column(db.Boolean, nullable=False)
    id_paquete = db.Column(db.Integer, db.ForeignKey('Paquete.id'), nullable=False)
    id_destinatario = db.Column(db.Integer, db.ForeignKey('Destinatario.id'), nullable=False)
    id_remitente = db.Column(db.Integer, db.ForeignKey('Remitente.id'), nullable=False)

    __table_args__ = (
        db.CheckConstraint("estado IN ('en preparación', 'en tránsito', 'en sucursal', 'en reparto', 'entregado')"),
        db.CheckConstraint("tipo_envio IN ('entrega en el día', 'entrega rápida', 'entrega normal')"),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'estado': self.estado,
            'recogida_a_domicilio': self.recogida_a_domicilio,
            'por_pagar': self.por_pagar,
            'tipo_envio': self.tipo_envio,
            'codigo_postal': self.codigo_postal,
            'fecha_recepcion': self.fecha_recepcion.isoformat(),
            'reparto_a_domicilio': self.reparto_a_domicilio.isoformat() if self.reparto_a_domicilio else None,
            'pagado': self.pagado,
            'id_paquete': self.id_paquete,
            'id_destinatario': self.id_destinatario,
            'id_remitente': self.id_remitente
        }
