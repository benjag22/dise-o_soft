from flask import Blueprint, request, jsonify
from database import db
from models import Remitente

# Crear un blueprint
remitente_bp = Blueprint('remitente', __name__)

class RemitenteAPI:
    def __init__(self, bd):
        self.bp = remitente_bp
        self.bd=bd
        self.register_routes()

    def register_routes(self):
        self.bp.add_url_rule('/remitentes', view_func=self.create_remitente, methods=['POST'])
        self.bp.add_url_rule('/remitentes', view_func=self.get_remitentes, methods=['GET'])
        self.bp.add_url_rule('/remitentes/<int:id>', view_func=self.get_remitente, methods=['GET'])
        self.bp.add_url_rule('/remitentes/<int:id>', view_func=self.update_remitente, methods=['PUT'])
        self.bp.add_url_rule('/remitentes/<int:id>', view_func=self.delete_remitente, methods=['DELETE'])

    def create_remitente(self):
        data = request.get_json()
        new_remitente = Remitente(
            rut_remitente=data['rut_remitente'],
            direccion=data['direccion'],
            correo=data['correo']
        )
        db.session.add(new_remitente)
        db.session.commit()
        return jsonify({'message': 'Remitente creado'}), 201

    def get_remitentes(self):
        remitentes = Remitente.query.all()
        return jsonify([remitente.to_dict() for remitente in remitentes])

    def get_remitente(self, id):
        remitente = Remitente.query.get(id)
        if remitente is None:
            return jsonify({'message': 'Remitente no encontrado'}), 404
        return jsonify(remitente.to_dict())

    def update_remitente(self, id):
        data = request.get_json()
        remitente = Remitente.query.get(id)
        if remitente is None:
            return jsonify({'message': 'Remitente no encontrado'}), 404
        remitente.direccion = data['direccion']
        remitente.correo = data['correo']
        db.session.commit()
        return jsonify({'message': 'Remitente actualizado'})

    def delete_remitente(self, id):
        remitente = Remitente.query.get(id)
        if remitente is None:
            return jsonify({'message': 'Remitente no encontrado'}), 404
        db.session.delete(remitente)
        db.session.commit()
        return jsonify({'message': 'Remitente eliminado'})
