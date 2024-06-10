from flask import Blueprint, request, jsonify
from database import db
from models import Paquete

# Crear un blueprint
paquete_bp = Blueprint('paquete', __name__)

class PaqueteAPI:
    def __init__(self, bd):
        self.bp = paquete_bp
        self.bd = bd
        self.register_routes()

    def register_routes(self):
        self.bp.add_url_rule('/paquetes', view_func=self.create_paquete, methods=['POST'])
        self.bp.add_url_rule('/paquetes', view_func=self.get_paquetes, methods=['GET'])
        self.bp.add_url_rule('/paquetes/<int:id>', view_func=self.get_paquete, methods=['GET'])
        self.bp.add_url_rule('/paquetes/<int:id>', view_func=self.update_paquete, methods=['PUT'])
        self.bp.add_url_rule('/paquetes/<int:id>', view_func=self.delete_paquete, methods=['DELETE'])

    def create_paquete(self):
        data = request.get_json()
        new_paquete = Paquete(
            tipo=data['tipo'],
            peso=data['peso'],
            fecha_ingreso=data['fecha_ingreso']
        )
        db.session.add(new_paquete)
        db.session.commit()
        return jsonify({'message': 'Paquete creado'}), 201

    def get_paquetes(self):
        paquetes = Paquete.query.all()
        return jsonify([paquete.to_dict() for paquete in paquetes])

    def get_paquete(self, id):
        paquete = Paquete.query.get(id)
        if paquete is None:
            return jsonify({'message': 'Paquete no encontrado'}), 404
        return jsonify(paquete.to_dict())

    def update_paquete(self, id):
        data = request.get_json()
        paquete = Paquete.query.get(id)
        if paquete is None:
            return jsonify({'message': 'Paquete no encontrado'}), 404
        paquete.tipo = data['tipo']
        paquete.peso = data['peso']
        paquete.fecha_ingreso = data['fecha_ingreso']
        db.session.commit()
        return jsonify({'message': 'Paquete actualizado'})

    def delete_paquete(self, id):
        paquete = Paquete.query.get(id)
        if paquete is None:
            return jsonify({'message': 'Paquete no encontrado'}), 404
        db.session.delete(paquete)
        db.session.commit()
        return jsonify({'message': 'Paquete eliminado'})
