from datetime import datetime
from database import db

# Modelo Paquete
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

# Modelo Cliente
class Cliente(db.Model):
    __tablename__ = 'Cliente'
    rut = db.Column(db.String(20), primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    ap_paterno = db.Column(db.String(50), nullable=False)
    ap_materno = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(10), nullable=False)
    remitente = db.relationship('Remitente', uselist=False, backref='cliente')
    destinatario = db.relationship('Destinatario', uselist=False, backref='cliente')
    
    __table_args__ = (
        db.CheckConstraint("estado IN ('activo', 'inactivo')"),
    )

# Modelo Destinatario
class Destinatario(db.Model):
    __tablename__ = 'Destinatario'
    id = db.Column(db.Integer, primary_key=True)
    rut_destinatario = db.Column(db.String(10), db.ForeignKey('Cliente.rut'), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(50), nullable=False)

# Modelo Remitente
class Remitente(db.Model):
    __tablename__ = 'Remitente'
    id = db.Column(db.Integer, primary_key=True)
    rut_remitente = db.Column(db.String(10), db.ForeignKey('Cliente.rut'), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(50), nullable=False)


class Envio(db.Model):
    __tablename__ = 'Envio'
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(20), nullable=False)
    recogida_a_domicilio = db.Column(db.Boolean, nullable=False)
    por_pagar = db.Column(db.Boolean, nullable=False)
    tipo_envio = db.Column(db.String(20), nullable=False)
    codigo_postal = db.Column(db.String(10), nullable=False)
    fecha_recepcion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reparto_a_domicilio = db.Column(db.DateTime, nullable=True)
    pagado = db.Column(db.Boolean, nullable=False)
    id_paquete = db.Column(db.Integer, db.ForeignKey('Paquete.id'), nullable=False)
    id_destinatario = db.Column(db.Integer, db.ForeignKey('Destinatario.id'), nullable=False)
    id_remitente = db.Column(db.Integer, db.ForeignKey('Remitente.id'), nullable=False)

    paquete = db.relationship('Paquete', backref='envios')
    destinatario = db.relationship('Destinatario', backref='envios')
    remitente = db.relationship('Remitente', backref='envios')

    __table_args__ = (
        db.CheckConstraint("estado IN ('en preparación', 'en tránsito', 'en sucursal', 'en reparto', 'entregado')"),
        db.CheckConstraint("tipo_envio IN ('entrega en el día', 'entrega rápida', 'entrega normal')"),
    )

# Modelo Historial
class Historial(db.Model):
    __tablename__ = 'Historial'
    id = db.Column(db.Integer, primary_key=True)
    fecha_mod = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    id_envio = db.Column(db.Integer, db.ForeignKey('Envio.id'), nullable=False)

    __table_args__ = (
        db.CheckConstraint("estado IN ('en preparación', 'en tránsito', 'en sucursal', 'en reparto', 'entregado')"),
    )