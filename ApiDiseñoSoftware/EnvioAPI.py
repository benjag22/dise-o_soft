from flask import Blueprint, request, jsonify
from database import db
from models import Envio

# Crear un blueprint
envio_bp = Blueprint('envio', __name__)

class EnvioAPI:
    def __init__(self, db):
        self.bp = envio_bp
        self.db=db
        self.register_routes()

    def register_routes(self):
        self.bp.add_url_rule('/envios', view_func=self.create_envio, methods=['POST'])
        self.bp.add_url_rule('/envios', view_func=self.get_envios, methods=['GET'])
        self.bp.add_url_rule('/envios/<int:id>', view_func=self.get_envio, methods=['GET'])
        self.bp.add_url_rule('/envios/<int:id>', view_func=self.update_envio, methods=['PUT'])
        self.bp.add_url_rule('/envios/<int:id>', view_func=self.delete_envio, methods=['DELETE'])

    def create_envio(self):
        data = request.get_json()
        new_envio = Envio(
            estado=data['estado'],
            recogida_a_domicilio=data['recogida_a_domicilio'],
            por_pagar=data['por_pagar'],
            tipo_envio=data['tipo_envio'],
            codigo_postal=data['codigo_postal'],
            fecha_recepcion=data['fecha_recepcion'],
            reparto_a_domicilio=data.get('reparto_a_domicilio'),
            pagado=data['pagado'],
            id_paquete=data['id_paquete'],
            id_destinatario=data['id_destinatario'],
            id_remitente=data['id_remitente']
        )
        db.session.add(new_envio)
        db.session.commit()
        return jsonify({'message': 'Envio creado'}), 201

    def get_envios(self):
        envios = Envio.query.all()
        return jsonify([envio.to_dict() for envio in envios])

    def get_envio(self, id):
        envio = Envio.query.get(id)
        if envio is None:
            return jsonify({'message': 'Envio no encontrado'}), 404
        return jsonify(envio.to_dict())

    def update_envio(self, id):
        data = request.get_json()
        envio = Envio.query.get(id)
        if envio is None:
            return jsonify({'message': 'Envio no encontrado'}), 404
        envio.estado = data['estado']
        envio.recogida_a_domicilio = data['recogida_a_domicilio']
        envio.por_pagar = data['por_pagar']
        envio.tipo_envio = data['tipo_envio']
        envio.codigo_postal = data['codigo_postal']
        envio.fecha_recepcion = data['fecha_recepcion']
        envio.reparto_a_domicilio = data.get('reparto_a_domicilio')
        envio.pagado = data['pagado']
        envio.id_paquete = data['id_paquete']
        envio.id_destinatario = data['id_destinatario']
        envio.id_remitente = data['id_remitente']
        db.session.commit()
        return jsonify({'message': 'Envio actualizado'})

    def delete_envio(self, id):
        envio = Envio.query.get(id)
        if envio is None:
            return jsonify({'message': 'Envio no encontrado'}), 404
        db.session.delete(envio)
        db.session.commit()
        return jsonify({'message': 'Envio eliminado'})

