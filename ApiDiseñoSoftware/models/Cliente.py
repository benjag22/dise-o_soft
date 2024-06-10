from database import db
class Cliente(db.Model):
    __tablename__ = 'Cliente'
    rut = db.Column(db.String(20), primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    nombre_primero = db.Column(db.String(50), nullable=False)
    nombre_segundo = db.Column(db.String(50), nullable=False)
    ap_paterno = db.Column(db.String(50), nullable=False)
    ap_materno = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(10), nullable=False)

    __table_args__ = (
        db.CheckConstraint("estado IN ('activo', 'inactivo')"),
    )

    def to_dict(self):
        return {
            'rut': self.rut,
            'fecha_creacion': self.fecha_creacion,
            'nombre_primero': self.nombre_primero,
            'nombre_segundo': self.nombre_segundo,
            'ap_paterno': self.ap_paterno,
            'ap_materno': self.ap_materno,
            'estado': self.estado
        }