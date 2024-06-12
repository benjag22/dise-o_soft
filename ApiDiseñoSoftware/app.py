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

@app.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json()
    if not data or not 'rut' in data or not 'nombre' in data or not 'ap_paterno' in data or not 'ap_materno' in data or not 'estado' in data:
        return jsonify({'message': 'Datos inválidos'}), 400

    new_cliente = Cliente(
        rut=data['rut'],
        fecha_creacion=datetime.utcnow(),
        nombre=data['nombre'],
        ap_paterno=data['ap_paterno'],
        ap_materno=data['ap_materno'],
        estado=data['estado']
    )
    db.session.add(new_cliente)
    db.session.commit()
    return jsonify({'rut': new_cliente.rut}), 201

@app.route('/clientes/<rut>', methods=['GET'])
def get_cliente(rut):
    cliente = Cliente.query.get(rut)
    if not cliente:
        return jsonify({'message': 'No se encontró el cliente'}), 404
    return jsonify({
        'rut': cliente.rut,
        'fecha_creacion': cliente.fecha_creacion,
        'nombre': cliente.nombre,
        'ap_paterno': cliente.ap_paterno,
        'ap_materno': cliente.ap_materno,
        'estado': cliente.estado
    })

@app.route('/remitentes', methods=['POST'])
def create_remitente():
    data = request.get_json()
    if not data or not 'rut_remitente' in data or not 'correo' in data or not 'direccion' in data:
        return jsonify({'message': 'Datos inválidos'}), 400

    cliente = Cliente.query.get(data['rut_remitente'])
    if not cliente:
        return jsonify({'message': 'Cliente no encontrado'}), 404

    new_remitente = Remitente(
        rut_remitente=data['rut_remitente'],
        correo=data['correo'],
        direccion=data['direccion']
    )
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

# Endpoint para buscar remitente por rut, dirección o correo
@app.route('/remitentes/buscar', methods=['GET'])
def buscar_remitente():
    rut = request.args.get('rut')
    direccion = request.args.get('direccion')
    correo = request.args.get('correo')
    
    if not rut and not direccion and not correo:
        return jsonify({'message': 'Faltan datos'}), 400

    remitente = Remitente.query.filter(
        (Remitente.rut_remitente == rut) | 
        (Remitente.direccion == direccion) |
        (Remitente.correo == correo)
    ).first()

    if not remitente:
        return jsonify({'message': 'No se encontró ningún remitente con esos datos'}), 404

    return jsonify({
        'id': remitente.id,
        'rut_remitente': remitente.rut_remitente,
        'correo': remitente.correo,
        'direccion': remitente.direccion
    }), 200

# Endpoint para crear un destinatario
@app.route('/destinatarios', methods=['POST'])
def create_destinatario():
    data = request.get_json()
    if not data or not 'rut_destinatario' in data or not 'telefono' in data or not 'direccion' in data or not 'correo' in data:
        return jsonify({'message': 'Datos inválidos'}), 400

    cliente = Cliente.query.get(data['rut_destinatario'])
    if not cliente:
        return jsonify({'message': 'Cliente no encontrado'}), 404

    new_destinatario = Destinatario(
        rut_destinatario=data['rut_destinatario'], 
        telefono=data['telefono'], 
        direccion=data['direccion'],
        correo=data['correo']
    )
    db.session.add(new_destinatario)
    db.session.commit()
    return jsonify({'message': 'Nuevo destinatario creado', 'id': new_destinatario.id}), 201

# Endpoint para obtener un destinatario por ID
@app.route('/destinatarios/<int:id>', methods=['GET'])
def get_destinatario(id):
    destinatario = Destinatario.query.get(id)
    if not destinatario:
        return jsonify({'message': 'No se encontró el destinatario'}), 404
    return jsonify({
        'id': destinatario.id,
        'rut_destinatario': destinatario.rut_destinatario,
        'telefono': destinatario.telefono,
        'direccion': destinatario.direccion,
        'correo': destinatario.correo
    })

# Endpoint para buscar destinatario por rut, dirección o teléfono
@app.route('/destinatarios/buscar', methods=['GET'])
def buscar_destinatario():
    rut = request.args.get('rut')
    direccion = request.args.get('direccion')
    telefono = request.args.get('telefono')
    
    if not rut and not direccion and not telefono:
        return jsonify({'message': 'Faltan datos'}), 400

    destinatario = Destinatario.query.filter(
        (Destinatario.rut_destinatario == rut) | 
        (Destinatario.direccion == direccion) |
        (Destinatario.telefono == telefono)
    ).first()

    if not destinatario:
        return jsonify({'message': 'No se encontró ningún destinatario con esos datos'}), 404

    return jsonify({
        'id': destinatario.id,
        'rut_destinatario': destinatario.rut_destinatario,
        'telefono': destinatario.telefono,
        'direccion': destinatario.direccion,
        'correo': destinatario.correo
    }), 200


@app.route('/paquetes/<int:id>', methods=['GET'])
def get_paquete(id):
    paquete = Paquete.query.get(id)
    if not paquete:
        return jsonify({'message': 'No se encontró el paquete'}), 404
    return jsonify({
        'id_paquete': paquete.id,
        'tipo': paquete.tipo,
        'peso': float(paquete.peso),
        'fecha_ingreso': paquete.fecha_ingreso
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

    new_paquete = Paquete(
        tipo=data['tipo'],
        peso=data['peso'],
        fecha_ingreso=datetime.utcnow()  # Agregar la fecha de ingreso al crear el paquete
    )
    db.session.add(new_paquete)
    db.session.commit()
    return jsonify({'message': 'Nuevo paquete creado', 'id_paquete': new_paquete.id}), 201


# Endpoint para crear un envío
@app.route('/envios', methods=['POST'])
def create_envio():
    data = request.get_json()
    
    required_fields = ['codigo_postal', 'tipo_envio', 'pagado', 'recogida_a_domicilio', 'por_pagar', 'id_paquete', 'id_remitente', 'id_destinatario']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Falta el campo {field}'}), 400

    if data['tipo_envio'] not in ['entrega en el día', 'entrega rápida', 'entrega normal']:
        return jsonify({'message': 'Tipo de envío inválido'}), 400

    # Comprobamos que las claves foráneas existan
    paquete = Paquete.query.get(data['id_paquete'])
    remitente = Remitente.query.get(data['id_remitente'])
    destinatario = Destinatario.query.get(data['id_destinatario'])

    if not paquete:
        return jsonify({'message': 'No se encontró el paquete'}), 404
    if not remitente:
        return jsonify({'message': 'No se encontró el remitente'}), 404
    if not destinatario:
        return jsonify({'message': 'No se encontró el destinatario'}), 404

    new_envio = Envio(
        codigo_postal=data['codigo_postal'],
        tipo_envio=data['tipo_envio'],
        pagado=data['pagado'],
        estado='en preparación',  # Estado inicial
        recogida_a_domicilio=data['recogida_a_domicilio'],
        fecha_recepcion=datetime.utcnow(),
        reparto_a_domicilio=data.get('reparto_a_domicilio'),  # Puede ser opcional
        por_pagar=data['por_pagar'],
        id_paquete=data['id_paquete'],
        id_remitente=data['id_remitente'],
        id_destinatario=data['id_destinatario']
    )
    db.session.add(new_envio)
    db.session.commit()
    return jsonify({'message': 'Nuevo envío creado', 'id_envio': new_envio.id}), 201


@app.route('/envios/<int:id>', methods=['GET'])
def get_envio(id):
    envio = Envio.query.get(id)
    if not envio:
        return jsonify({'message': 'No se encontró el envío'}), 404

    paquete = Paquete.query.get(envio.id_paquete)
    remitente = Remitente.query.get(envio.id_remitente)
    destinatario = Destinatario.query.get(envio.id_destinatario)

    return jsonify({
        'id_envio': envio.id,
        'estado': envio.estado,
        'recogida_a_domicilio': envio.recogida_a_domicilio,
        'por_pagar': envio.por_pagar,
        'tipo_envio': envio.tipo_envio,
        'codigo_postal': envio.codigo_postal,
        'fecha_recepcion': envio.fecha_recepcion,
        'reparto_a_domicilio': envio.reparto_a_domicilio,
        'pagado': envio.pagado,
        'paquete': {
            'id_paquete': paquete.id,
            'tipo': paquete.tipo,
            'peso': float(paquete.peso),
            'fecha_ingreso': paquete.fecha_ingreso
        },
        'remitente': {
            'id_remitente': remitente.id,
            'rut_remitente': remitente.rut_remitente,
            'telefono': remitente.telefono,
            'direccion': remitente.direccion,
            'correo': remitente.correo
        },
        'destinatario': {
            'id_destinatario': destinatario.id,
            'rut_destinatario': destinatario.rut_destinatario,
            'telefono': destinatario.telefono,
            'direccion': destinatario.direccion,
            'correo': destinatario.correo
        }
    }), 200


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)


