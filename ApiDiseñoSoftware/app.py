from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:.@localhost:5432/envios'

db = SQLAlchemy(app)
# Modelo Paquete
class Paquete(db.Model):
    __tablename__ = 'paquete'
    id_paquete = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    peso = db.Column(db.Float, nullable=False)

    __table_args__ = (
        db.CheckConstraint("tipo IN ('sobre', 'encomienda')"),
        db.CheckConstraint("peso > 0"),
    )

# Modelo Cliente
class Cliente(db.Model):
    __tablename__ = 'cliente'
    rut = db.Column(db.String(10), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

# Modelo Destinatario
class Destinatario(db.Model):
    __tablename__ = 'destinatario'
    id = db.Column(db.Integer, primary_key=True)
    rut_cliente = db.Column(db.String(10), db.ForeignKey('cliente.rut'))
    telefono = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    cliente = db.relationship('Cliente', backref='destinatarios')

# Modelo Remitente
class Remitente(db.Model):
    __tablename__ = 'remitente'
    id = db.Column(db.Integer, primary_key=True)
    rut_cliente = db.Column(db.String(10), db.ForeignKey('cliente.rut'))
    correo = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    cliente = db.relationship('Cliente', backref='remitentes')

# Modelo Envio
class Envio(db.Model):
    __tablename__ = 'envio'
    id_envio = db.Column(db.Integer, primary_key=True)
    cod_postal = db.Column(db.String(10), nullable=False)
    tipo_envio = db.Column(db.String(20), nullable=False)
    pagado = db.Column(db.Boolean, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='En preparación')
    recogida_a_domicilio = db.Column(db.Boolean, nullable=False)
    por_pagar = db.Column(db.Boolean, nullable=False)
    id_paquete = db.Column(db.Integer, db.ForeignKey('paquete.id_paquete'), nullable=False)
    id_remitente = db.Column(db.Integer, db.ForeignKey('remitente.id'), nullable=False)
    id_destinatario = db.Column(db.Integer, db.ForeignKey('destinatario.id'), nullable=False)

    __table_args__ = (
        db.CheckConstraint("tipo_envio IN ('Entrega en el dia', 'Entrega rapida', 'Entrega normal')"),
        db.CheckConstraint("pagado IN (0, 1)"),
        db.CheckConstraint("estado IN ('En preparación', 'En tránsito', 'En sucursal', 'En reparto', 'Entregado')"),
        db.CheckConstraint("recogida_a_domicilio IN (0, 1)"),
        db.CheckConstraint("por_pagar IN (0, 1)")
    )

# Modelo Historial
class Historial(db.Model):
    __tablename__ = 'historial'
    id_historial = db.Column(db.Integer, primary_key=True)
    fecha_mod = db.Column(db.DateTime, nullable=False)
    id_envio = db.Column(db.Integer, db.ForeignKey('envio.id_envio'), nullable=False)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)


