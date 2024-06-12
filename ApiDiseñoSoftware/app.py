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
    cliente = Cliente.query.filter_by(rut=rut).first()
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
    
    if not rut or not direccion or not correo:
        return jsonify({'message': 'Faltan datos'}), 400

    # Utilizar filter en lugar de filter_by para aplicar múltiples condiciones
    remitente = Remitente.query.filter(
        (Remitente.rut_remitente == rut) & 
        (Remitente.direccion == direccion) &
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
    
    if not rut or not direccion or not telefono:
        return jsonify({'message': 'Faltan datos'}), 400

    # Utilizar filter en lugar de filter_by para aplicar múltiples condiciones
    destinatario = Destinatario.query.filter(
        (Destinatario.rut_destinatario == rut) & 
        (Destinatario.direccion == direccion) &
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

@app.route('/paquetes/buscar', methods=['GET'])
def buscar_paquete():
    tipo = request.args.get('tipo')
    peso = request.args.get('peso')
    
    if not tipo or not peso:
        return jsonify({'message': 'Faltan datos'}), 400

    # Utilizar filter en lugar de filter_by para aplicar múltiples condiciones
    paquete = Paquete.query.filter(
        (Paquete.tipo == tipo) & 
        (Paquete.peso == peso)
    ).first()

    if not paquete:
        return jsonify({'message': 'No se encontró ningún paquete con esos datos'}), 404

    return jsonify({
        'id_paquete': paquete.id,
        'tipo': paquete.tipo,
        'peso': float(paquete.peso),
        'fecha_ingreso': paquete.fecha_ingreso
    }), 200


@app.route('/paquetes', methods=['POST'])
def create_paquete():
    data = request.get_json()

    if not data or 'tipo' not in data or 'peso' not in data:
        return jsonify({'message': 'Datos inválidos. Se requiere "tipo" y "peso".'}), 400

    tipo = data['tipo']
    peso = data['peso']

    if tipo not in ['sobre', 'encomienda']:
        return jsonify({'message': 'Tipo de paquete inválido. Debe ser "sobre" o "encomienda".'}), 400

    if not isinstance(peso, (int, float)) or peso <= 0:
        return jsonify({'message': 'Peso inválido. Debe ser un número mayor que 0.'}), 400

    nuevo_paquete = Paquete(tipo=tipo, peso=peso, fecha_ingreso=datetime.utcnow())
    db.session.add(nuevo_paquete)
    db.session.commit()

    return jsonify({'message': 'Nuevo paquete creado', 'id_paquete': nuevo_paquete.id}), 201

@app.route('/paquetes/<int:id_paquete>', methods=['GET'])
def get_paquete(id_paquete):
    paquete = Paquete.query.get_or_404(id_paquete)
    return jsonify({
        'id': paquete.id,
        'tipo': paquete.tipo,
        'peso': float(paquete.peso),  # Convertir Decimal a float
        'fecha_ingreso': paquete.fecha_ingreso.isoformat()
    })

@app.route('/envios', methods=['POST'])
def create_envio():
    data = request.get_json()

    required_fields = [
        "codigo_postal", "tipo_envio", "pagado", "recogida_a_domicilio",
        "por_pagar", "id_paquete", "id_remitente", "id_destinatario"
    ]
    for field in required_fields:
        if field not in data:
            print(f'Falta el campo "{field}"')
            return jsonify({'message': f'Falta el campo "{field}"'}), 400

    if data['tipo_envio'] not in ['entrega en el día', 'entrega rápida', 'entrega normal']:
        print('Tipo de envío inválido')
        return jsonify({'message': 'Tipo de envío inválido'}), 400

    for field in ["id_paquete", "id_remitente", "id_destinatario"]:
        if not isinstance(data[field], int):
            print(f'El campo "{field}" debe ser un entero')
            return jsonify({'message': f'El campo "{field}" debe ser un entero'}), 400

    for field in ["pagado", "recogida_a_domicilio", "por_pagar"]:
        if not isinstance(data[field], bool):
            print(f'El campo "{field}" debe ser un booleano')
            return jsonify({'message': f'El campo "{field}" debe ser un booleano'}), 400

    nuevo_envio = Envio(
        codigo_postal=data['codigo_postal'],
        tipo_envio=data['tipo_envio'],
        pagado=data['pagado'],
        recogida_a_domicilio=data['recogida_a_domicilio'],
        por_pagar=data['por_pagar'],
        id_paquete=data['id_paquete'],
        id_remitente=data['id_remitente'],
        id_destinatario=data['id_destinatario'],
        estado='en preparación', 
        fecha_recepcion=datetime.utcnow()
    )
    db.session.add(nuevo_envio)
    db.session.commit()

    return jsonify({'message': 'Nuevo envío creado', 'id_envio': nuevo_envio.id}), 201


@app.route('/envios/<int:envio_id>', methods=['GET'])
def get_envio_by_id(envio_id):
    try:
        envio = Envio.query.get(envio_id)
        if not envio:
            return jsonify({'error': 'Envío no encontrado'}), 404

        paquete = Paquete.query.get(envio.id_paquete)
        remitente = Remitente.query.get(envio.id_remitente)
        destinatario = Destinatario.query.get(envio.id_destinatario)
        nombre_remitente = Cliente.query.get(remitente.rut_remitente)
        nombre_destinatario = Cliente.query.get(destinatario.rut_destinatario)

        resultado = {
            'id_envio': envio.id,
            'estado': envio.estado,
            'recogida_a_domicilio': envio.recogida_a_domicilio,
            'por_pagar': envio.por_pagar,
            'tipo_envio': envio.tipo_envio,
            'codigo_postal': envio.codigo_postal,
            'fecha_recepcion': envio.fecha_recepcion.isoformat() if envio.fecha_recepcion else None,
            'reparto_a_domicilio': envio.reparto_a_domicilio.isoformat() if envio.reparto_a_domicilio else None,
            'pagado': envio.pagado,
            'paquete': {
                'id_paquete': paquete.id,
                'tipo': paquete.tipo,
                'peso': float(paquete.peso) if paquete.peso else None,
                'fecha_ingreso': paquete.fecha_ingreso.isoformat() if paquete.fecha_ingreso else None
            },
            'remitente': {
                'id_remitente': remitente.id,
                'rut_remitente': remitente.rut_remitente,
                'nombre': nombre_remitente.nombre if nombre_remitente else None,
                'direccion': remitente.direccion,
                'correo': remitente.correo
            },
            'destinatario': {
                'id_destinatario': destinatario.id,
                'rut_destinatario': destinatario.rut_destinatario,
                'nombre': nombre_destinatario.nombre if nombre_destinatario else None,
                'telefono': destinatario.telefono,
                'direccion': destinatario.direccion,
                'correo': destinatario.correo
            }
        }
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/envios/por_pagar', methods=['GET'])
def get_envios_por_pagar():
    try:
        envios_por_pagar = Envio.query.filter_by(por_pagar=True).all()

        resultados = []
        for envio in envios_por_pagar:
            paquete = Paquete.query.get(envio.id_paquete)
            remitente = Remitente.query.get(envio.id_remitente)
            destinatario = Destinatario.query.get(envio.id_destinatario)
            nombre_remitente = Cliente.query.get(remitente.rut_remitente)
            nombre_destinatario = Cliente.query.get(destinatario.rut_destinatario)

            resultados.append({
                'id_envio': envio.id,
                'estado': envio.estado,
                'recogida_a_domicilio': envio.recogida_a_domicilio,
                'por_pagar': envio.por_pagar,
                'tipo_envio': envio.tipo_envio,
                'codigo_postal': envio.codigo_postal,
                'fecha_recepcion': envio.fecha_recepcion.isoformat() if envio.fecha_recepcion else None,
                'reparto_a_domicilio': envio.reparto_a_domicilio.isoformat() if envio.reparto_a_domicilio else None,
                'pagado': envio.pagado,
                'paquete': {
                    'id_paquete': paquete.id,
                    'tipo': paquete.tipo,
                    'peso': float(paquete.peso) if paquete.peso else None,
                    'fecha_ingreso': paquete.fecha_ingreso.isoformat() if paquete.fecha_ingreso else None
                },
                'remitente': {
                    'id_remitente': remitente.id,
                    'rut_remitente': remitente.rut_remitente,
                    'nombre': nombre_remitente.nombre if nombre_remitente else None,
                    'direccion': remitente.direccion,
                    'correo': remitente.correo
                },
                'destinatario': {
                    'id_destinatario': destinatario.id,
                    'rut_destinatario': destinatario.rut_destinatario,
                    'nombre': nombre_destinatario.nombre if nombre_destinatario else None,
                    'telefono': destinatario.telefono,
                    'direccion': destinatario.direccion,
                    'correo': destinatario.correo
                }
            })

        return jsonify(resultados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)


