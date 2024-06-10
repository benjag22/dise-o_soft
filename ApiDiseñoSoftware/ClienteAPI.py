# ClienteAPI.py
from flask import Blueprint, request, jsonify
from database import db
from models import Cliente

cliente_bp = Blueprint('cliente', __name__)

class ClienteAPI:
    def __init__(self, db):
        self.db = db
        self.bp = cliente_bp
        self.register_routes()


    def register_routes(self):
        self.bp.add_url_rule('/clientes', view_func=self.create_cliente, methods=['POST'])
        self.bp.add_url_rule('/clientes', view_func=self.get_clientes, methods=['GET'])
        self.bp.add_url_rule('/clientes/<rut>', view_func=self.get_cliente, methods=['GET'])
        self.bp.add_url_rule('/clientes/<rut>', view_func=self.update_cliente, methods=['PUT'])
        self.bp.add_url_rule('/clientes/<rut>', view_func=self.delete_cliente, methods=['DELETE'])

    def create_cliente(self):
        data = request.get_json()
        new_cliente = Cliente(
            rut=data['rut'],
            fecha_creacion=data['fecha_creacion'],
            nombre_primero=data['nombre_primero'],
            nombre_segundo=data['nombre_segundo'],
            ap_paterno=data['ap_paterno'],
            ap_materno=data['ap_materno'],
            estado=data['estado']
        )
        db.session.add(new_cliente)
        db.session.commit()
        return jsonify({'message': 'Cliente creado'}), 201

    def get_clientes(self):
        clientes = db.session.query(Cliente).all() # Use db.session.query
        return jsonify([cliente.to_dict() for cliente in clientes])

    def get_cliente(self, rut):
        cliente = Cliente.query.get(rut)
        if cliente is None:
            return jsonify({'message': 'Cliente no encontrado'}), 404
        return jsonify(cliente.to_dict())

    def update_cliente(self, rut):
        data = request.get_json()
        cliente = Cliente.query.get(rut)
        if cliente is None:
            return jsonify({'message': 'Cliente no encontrado'}), 404
        cliente.nombre_primero = data['nombre_primero']
        cliente.nombre_segundo = data['nombre_segundo']
        cliente.ap_paterno = data['ap_paterno']
        cliente.ap_materno = data['ap_materno']
        cliente.estado = data['estado']
        db.session.commit()
        return jsonify({'message': 'Cliente actualizado'})

    def delete_cliente(self, rut):
        cliente = Cliente.query.get(rut)
        if cliente is None:
            return jsonify({'message': 'Cliente no encontrado'}), 404
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({'message': 'Cliente eliminado'})