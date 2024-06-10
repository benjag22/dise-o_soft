from flask import Blueprint, request, jsonify
from database import db
from models import Historial

# Crear un blueprint
historial_bp = Blueprint('historial', __name__)

class HistorialAPI:
    def __init__(self, db):
        self.bp = historial_bp
        self.db=db
        self.register_routes()

    def register_routes(self):
        self.bp.add_url_rule('/historial', view_func=self.create_historial, methods=['POST'])
        self.bp.add_url_rule('/historial', view_func=self.get_historiales, methods=['GET'])
        self.bp.add_url_rule('/historial/<int:id>', view_func=self.get_historial, methods=['GET'])
        self.bp.add_url_rule('/historial/<int:id>', view_func=self.update_historial, methods=['PUT'])
        self.bp.add_url_rule('/historial/<int:id>', view_func=self.delete_historial, methods=['DELETE'])

    def create_historial(self):
        data = request.get_json()
        new_historial = Historial(
            fecha_mod=data['fecha_mod'],
            estado=data['estado'],
            id_envio=data['id_envio']
        )
        db.session.add(new_historial)
        db.session.commit()
        return jsonify({'message': 'Historial creado'}), 201

    def get_historiales(self):
        historiales = Historial.query.all()
        return jsonify([historial.to_dict() for historial in historiales])

    def get_historial(self, id):
        historial = Historial.query.get(id)
        if historial is None:
            return jsonify({'message': 'Historial no encontrado'}), 404
        return jsonify(historial.to_dict())

    def update_historial(self, id):
        data = request.get_json()
        historial = Historial.query.get(id)
        if historial is None:
            return jsonify({'message': 'Historial no encontrado'}), 404
        historial.fecha_mod = data['fecha_mod']
        historial.estado = data['estado']
        historial.id_envio = data['id_envio']
        db.session.commit()
        return jsonify({'message': 'Historial actualizado'})

    def delete_historial(self, id):
        historial = Historial.query.get(id)
        if historial is None:
            return jsonify({'message': 'Historial no encontrado'}), 404
        db.session.delete(historial)
        db.session.commit()
        return jsonify({'message': 'Historial eliminado'})
