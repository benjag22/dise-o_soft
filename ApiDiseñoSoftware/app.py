from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:.@localhost:5432/envios'

db = SQLAlchemy(app)
# Modelo Paquete
class Paquete(db.Model):
    __tablename__ = 'Paquete'
    id_paquete = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    peso = db.Column(db.Float, nullable=False)

    __table_args__ = (
        db.CheckConstraint("tipo IN ('sobre', 'encomienda')"),
        db.CheckConstraint("peso > 0"),
    )

# Modelo Cliente
class Cliente(db.Model):
    __tablename__ = 'Cliente'
    rut = db.Column(db.String(10), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    remitente = db.relationship('Remitente', uselist=False, backref='cliente')
    destinatario = db.relationship('Destinatario', uselist=False, backref='cliente')

# Modelo Destinatario
class Destinatario(db.Model):
    __tablename__ = 'Destinatario'
    id = db.Column(db.Integer, primary_key=True)
    rut_destinatario = db.Column(db.String(10), db.ForeignKey('Cliente.rut'), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)

# Modelo Remitente
class Remitente(db.Model):
    __tablename__ = 'Remitente'
    id = db.Column(db.Integer, primary_key=True)
    rut_remitente = db.Column(db.String(10), db.ForeignKey('Cliente.rut'), nullable=False)
    correo = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)


# Modelo Envio
class Envio(db.Model):
    __tablename__ = 'Envio'
    id_envio = db.Column(db.Integer, primary_key=True)
    cod_postal = db.Column(db.String(10), nullable=False)
    tipo_envio = db.Column(db.String(20), nullable=False)
    pagado = db.Column(db.Boolean, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='En preparación')
    recogida_a_domicilio = db.Column(db.Boolean, nullable=False)
    reparto_a_domicilio = db.Column(db.Boolean, nullable=False)
    fecha_recepcion =db.Column(db.DateTime, nullable=False)
    por_pagar = db.Column(db.Boolean, nullable=False)
    id_paquete = db.Column(db.Integer, db.ForeignKey('Paquete.id_paquete'), nullable=False)
    id_remitente = db.Column(db.Integer, db.ForeignKey('Remitente.id'), nullable=False)
    id_destinatario = db.Column(db.Integer, db.ForeignKey('Destinatario.id'), nullable=False)

    __table_args__ = (
        db.CheckConstraint("tipo_envio IN ('Entrega en el dia', 'Entrega rapida', 'Entrega normal')"),
        db.CheckConstraint("estado IN ('En preparación', 'En tránsito', 'En sucursal', 'En reparto', 'Entregado')"),
    )

# Modelo Historial
class Historial(db.Model):
    __tablename__ = 'Historial'
    id_historial = db.Column(db.Integer, primary_key=True)
    fecha_mod = db.Column(db.DateTime, nullable=False)
    id_envio = db.Column(db.Integer, db.ForeignKey('Envio.id_envio'), nullable=False)

@app.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json()
    if not data or not 'rut' in data or not 'nombre' in data:
        return jsonify({'message': 'Datos inválidos'}), 400

    new_cliente = Cliente(rut=data['rut'], nombre=data['nombre'])
    db.session.add(new_cliente)
    db.session.commit()
    return jsonify({'rut': new_cliente.rut, 'nombre': new_cliente.nombre}), 201

@app.route('/clientes/<rut>', methods=['GET'])
def get_cliente(rut):
    cliente = Cliente.query.get(rut)
    if not cliente:
        return jsonify({'message': 'No se encontró el cliente'}), 404
    return jsonify({'rut': cliente.rut, 'nombre': cliente.nombre})

@app.route('/remitentes', methods=['POST'])
def create_remitente():
    data = request.get_json()
    if not data or not 'rut_remitente' in data or not 'correo' in data or not 'direccion' in data:
        return jsonify({'message': 'Datos inválidos'}), 400

    remitente = Remitente.query.filter_by(rut_remitente=data['rut_remitente']).first()
    if remitente:
        return jsonify({'message': 'Remitente ya existe'}), 400

    new_remitente = Remitente(rut_remitente=data['rut_remitente'], correo=data['correo'], direccion=data['direccion'])
    db.session.add(new_remitente)
    db.session.commit()
    return jsonify({'message': 'Nuevo remitente creado', 'id': new_remitente.id}), 201


@app.route('/remitentes/<int:id>', methods=['GET'])
def get_remitente(id):
    remitente = Remitente.query.get(id)
    if not remitente:
        return jsonify({'message': 'No se encontró el remitente'}), 404
    return jsonify({
        'id': remitente.id,
        'rut_remitente': remitente.rut_remitente,
        'correo': remitente.correo,
        'direccion': remitente.direccion
    })

@app.route('/remitentes/buscar', methods=['GET'])
def buscar_remitente():
    rut = request.args.get('rut')
    direccion = request.args.get('direccion')
    correo = request.args.get('correo')
    
    if not rut or not direccion or not correo:
        return jsonify({'message': 'Faltan datos'}), 400

    remitente = Remitente.query.filter_by(
        rut_remitente=rut,
        direccion=direccion,
        correo=correo
    ).first()

    if not remitente:
        return jsonify({'message': 'No se encontró ningún remitente con esos datos'}), 404

    return jsonify({
        'id': remitente.id,
        'rut_remitente': remitente.rut_remitente,
        'correo': remitente.correo,
        'direccion': remitente.direccion
    }), 200


@app.route('/destinatarios', methods=['POST'])
def create_destinatario():
    data = request.get_json()
    if not data or not 'rut_destinatario' in data or not 'telefono' in data or not 'direccion' in data:
        return jsonify({'message': 'Datos inválidos'}), 400

    cliente = Cliente.query.get(data['rut_destinatario'])
    if not cliente:
        return jsonify({'message': 'Cliente no encontrado'}), 404

    new_destinatario = Destinatario(rut_destinatario=data['rut_destinatario'], telefono=data['telefono'], direccion=data['direccion'])
    db.session.add(new_destinatario)
    db.session.commit()
    return jsonify({'message': 'Nuevo destinatario creado', 'id': new_destinatario.id}), 201


@app.route('/destinatarios/<int:id>', methods=['GET'])
def get_destinatario(id):
    destinatario = Destinatario.query.get(id)
    if not destinatario:
        return jsonify({'message': 'No se encontró el destinatario'}), 404
    return jsonify({
        'id': destinatario.id,
        'rut_destinatario': destinatario.rut_destinatario,
        'telefono': destinatario.telefono,
        'direccion': destinatario.direccion
    })

@app.route('/destinatarios/buscar', methods=['GET'])
def buscar_destinatario():
    rut = request.args.get('rut')
    direccion = request.args.get('direccion')
    telefono = request.args.get('telefono')
    
    if not rut or not direccion or not telefono:
        return jsonify({'message': 'Faltan datos'}), 400

    destinatario = Destinatario.query.filter_by(
        rut_destinatario=rut,
        direccion=direccion,
        telefono=telefono
    ).first()

    if not destinatario:
        return jsonify({'message': 'No se encontró ningún destinatario con esos datos'}), 404

    return jsonify({
        'id': destinatario.id,
        'rut_destinatario': destinatario.rut_destinatario,
        'telefono': destinatario.telefono,
        'direccion': destinatario.direccion
    }), 200


@app.route('/paquetes/<int:id>', methods=['GET'])
def get_paquete(id):
    paquete = Paquete.query.get(id)
    if not paquete:
        return jsonify({'message': 'No se encontró el paquete'}), 404
    return jsonify({
        'id_paquete': paquete.id_paquete,
        'tipo': paquete.tipo,
        'peso': paquete.peso
    })

@app.route('/paquetes', methods=['POST'])
def create_paquete():
    data = request.get_json()
    if not data or not 'tipo' in data or not 'peso' in data:
        return jsonify({'message': 'Datos inválidos'}), 400

    if data['tipo'] not in ['sobre', 'encomienda']:
        return jsonify({'message': 'Tipo de paquete inválido'}), 400

    if data['peso'] <= 0:
        return jsonify({'message': 'El peso debe ser mayor a 0'}), 400

    new_paquete = Paquete(tipo=data['tipo'], peso=data['peso'])
    db.session.add(new_paquete)
    db.session.commit()
    return jsonify({'message': 'Nuevo paquete creado', 'id_paquete': new_paquete.id_paquete}), 201

@app.route('/envios', methods=['POST'])
def create_envio():
    data = request.get_json()
    required_fields = ['cod_postal', 'tipo_envio', 'pagado', 'recogida_a_domicilio', 'reparto_a_domicilio', 'por_pagar', 'id_paquete', 'id_remitente', 'id_destinatario']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Falta el campo {field}'}), 400

    if data['tipo_envio'] not in ['Entrega en el dia', 'Entrega rapida', 'Entrega normal']:
        return jsonify({'message': 'Tipo de envío inválido'}), 400

    new_envio = Envio(
        cod_postal=data['cod_postal'],
        tipo_envio=data['tipo_envio'],
        pagado=data['pagado'],
        estado='En preparación',  # Estado inicial
        recogida_a_domicilio=data['recogida_a_domicilio'],
        reparto_a_domicilio=data['reparto_a_domicilio'],
        fecha_recepcion=datetime.utcnow(),
        por_pagar=data['por_pagar'],
        id_paquete=data['id_paquete'],
        id_remitente=data['id_remitente'],
        id_destinatario=data['id_destinatario']
    )
    db.session.add(new_envio)
    db.session.commit()
    return jsonify({'message': 'Nuevo envío creado', 'id_envio': new_envio.id_envio}), 201


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)


