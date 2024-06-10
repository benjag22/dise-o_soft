from flask import Blueprint, request, jsonify
from database import db
from models import Destinatario

# Crear un blueprint
destinatario_bp = Blueprint('destinatario', __name__)

class DestinatarioAPI:
    def __init__(self, db):
        self.bp = destinatario_bp
        self.db = db
        self.register_routes()

    def register_routes(self):
        self.bp.add_url_rule('/destinatarios', view_func=self.create_destinatario, methods=['POST'])
        self.bp.add_url_rule('/destinatarios', view_func=self.get_destinatarios, methods=['GET'])
        self.bp.add_url_rule('/destinatarios/<int:id>', view_func=self.get_destinatario, methods=['GET'])
        self.bp.add_url_rule('/destinatarios/<int:id>', view_func=self.update_destinatario, methods=['PUT'])
        self.bp.add_url_rule('/destinatarios/<int:id>', view_func=self.delete_destinatario, methods=['DELETE'])

    def create_destinatario(self):
        data = request.get_json()
        new_destinatario = Destinatario(
            rut_destinatario=data['rut_destinatario'],
            telefono=data['telefono'],
            direccion=data['direccion'],
            correo=data['correo']
        )
        db.session.add(new_destinatario)
        db.session.commit()
        return jsonify({'message': 'Destinatario creado'}), 201

    def get_destinatarios(self):
        destinatarios = Destinatario.query.all()
        return jsonify([destinatario.to_dict() for destinatario in destinatarios])

    def get_destinatario(self, id):
        destinatario = Destinatario.query.get(id)
        if destinatario is None:
            return jsonify({'message': 'Destinatario no encontrado'}), 404
        return jsonify(destinatario.to_dict())

    def update_destinatario(self, id):
        data = request.get_json()
        destinatario = Destinatario.query.get(id)
        if destinatario is None:
            return jsonify({'message': 'Destinatario no encontrado'}), 404
        destinatario.telefono = data['telefono']
        destinatario.direccion = data['direccion']
        destinatario.correo = data['correo']
        db.session.commit()
        return jsonify({'message': 'Destinatario actualizado'})

    def delete_destinatario(self, id):
        destinatario = Destinatario.query.get(id)
        if destinatario is None:
            return jsonify({'message': 'Destinatario no encontrado'}), 404
        db.session.delete(destinatario)
        db.session.commit()
        return jsonify({'message': 'Destinatario eliminado'})
