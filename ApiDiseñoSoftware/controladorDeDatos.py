from flask import jsonify, request
from datetime import datetime
import validadorDeDatos as vdd
from database import db, app
import ventanaDeErrores as vde
from parametros import Parametros
from decimal import Decimal

@app.route("/clientes", methods=["POST"])
def create_cliente():
    data = request.get_json()
    errores = vde.clientes_error_post(data)
    if errores:
        return jsonify({"message": "Datos inválidos", "errores": errores}), 400

    new_cliente = vdd.Cliente(
        rut=data["rut"],
        fecha_creacion=datetime.utcnow(),
        nombre=data["nombre"],
        ap_paterno=data["ap_paterno"],
        ap_materno=data["ap_materno"],
        estado=data["estado"],
    )
    db.session.add(new_cliente)
    db.session.commit()
    return jsonify({"rut": new_cliente.rut}), 201


@app.route("/clientes/<rut>", methods=["GET"])
def get_cliente(rut):
    errores = vde.cliente_error_get(rut)
    if errores:
        return jsonify({"message": "Datos inválidos", "errores": errores}), 404

    cliente = vdd.Cliente.query.filter_by(rut=rut).first()
    return jsonify(
        {
            "rut": cliente.rut,
            "fecha_creacion": cliente.fecha_creacion,
            "nombre": cliente.nombre,
            "ap_paterno": cliente.ap_paterno,
            "ap_materno": cliente.ap_materno,
            "estado": cliente.estado,
        }
    )


@app.route("/remitentes", methods=["POST"])
def create_remitente():
    data = request.get_json()
    errores = vde.remitentes_error_post(data)
    if errores:
        return jsonify({"message": "Datos inválidos", "errores": errores}), 400

    cliente = vdd.Cliente.query.get(data["rut_remitente"])
    if not cliente:
        return jsonify({"message": "Cliente no encontrado"}), 404

    new_remitente = vdd.Remitente(
        rut_remitente=data["rut_remitente"],
        correo=data["correo"],
        direccion=data["direccion"],
    )
    db.session.add(new_remitente)
    db.session.commit()
    return jsonify({"message": "Nuevo remitente creado", "id": new_remitente.id}), 201


@app.route("/remitentes/<int:id>", methods=["GET"])
def get_remitente(id):
    remitente = vdd.Remitente.query.get(id)
    errores = vde.remitente_error_get(remitente)
    if errores:
        return jsonify(
            {"message": "Error al obtener el remitente", "errores": errores}
        ), 404

    return jsonify(
        {
            "id": remitente.id,
            "rut_remitente": remitente.rut_remitente,
            "correo": remitente.correo,
            "direccion": remitente.direccion,
        }
    )


# Endpoint para buscar remitente por rut, dirección o correo
@app.route("/remitentes/buscar", methods=["GET"])
def buscar_remitente():
    rut = request.args.get("rut")
    direccion = request.args.get("direccion")
    correo = request.args.get("correo")

    errores = vde.buscar_remitente_error_get(rut, direccion, correo)
    if errores:
        return jsonify({"message": "Error en la solicitud", "errores": errores}), 400

    remitente = vdd.Remitente.query.filter(
        (vdd.Remitente.rut_remitente == rut)
        & (vdd.Remitente.direccion == direccion)
        & (vdd.Remitente.correo == correo)
    ).first()

    if not remitente:
        return jsonify(
            {"message": "No se encontró ningún remitente con esos datos"}
        ), 404

    return jsonify(
        {
            "id": remitente.id,
            "rut_remitente": remitente.rut_remitente,
            "correo": remitente.correo,
            "direccion": remitente.direccion,
        }
    ), 200


# Endpoint para crear un destinatario
@app.route("/destinatarios", methods=["POST"])
def create_destinatario():
    data = request.get_json()
    errores = vde.destinatario_error_post(data)
    if errores:
        return jsonify({"message": "Datos inválidos", "errores": errores}), 400

    cliente = vdd.Cliente.query.get(data["rut_destinatario"])
    if not cliente:
        return jsonify({"message": "Cliente no encontrado"}), 404

    new_destinatario = vdd.Destinatario(
        rut_destinatario=data["rut_destinatario"],
        telefono=data["telefono"],
        direccion=data["direccion"],
        correo=data["correo"],
    )
    db.session.add(new_destinatario)
    db.session.commit()
    return jsonify(
        {"message": "Nuevo destinatario creado", "id": new_destinatario.id}
    ), 201


# Endpoint para obtener un destinatario por ID
@app.route("/destinatarios/<int:id>", methods=["GET"])
def get_destinatario(id):
    destinatario = vdd.Destinatario.query.get(id)
    errores = vde.destinatario_error_get(destinatario)
    if errores:
        return jsonify(
            {"message": "Error al obtener el destinatario", "errores": errores}
        ), 404

    return jsonify(
        {
            "id": destinatario.id,
            "rut_destinatario": destinatario.rut_destinatario,
            "telefono": destinatario.telefono,
            "direccion": destinatario.direccion,
            "correo": destinatario.correo,
        }
    )


# Endpoint para buscar destinatario por rut, dirección o teléfono
@app.route("/destinatarios/buscar", methods=["GET"])
def buscar_destinatario():
    rut = request.args.get("rut")
    direccion = request.args.get("direccion")
    telefono = request.args.get("telefono")

    # Consultar destinatario
    destinatario = vdd.Destinatario.query.filter(
        (vdd.Destinatario.rut_destinatario == rut)
        & (vdd.Destinatario.direccion == direccion)
        & (vdd.Destinatario.telefono == telefono)
    ).first()

    # Manejar el caso donde no se encuentra el destinatario
    errores = vde.destinatario_error_buscar(rut, direccion, telefono, destinatario)
    if errores:
        return jsonify(
            {"message": "Error en la búsqueda de destinatario", "errores": errores}
        ), 404

    # Devolver el destinatario encontrado
    return jsonify(
        {
            "id": destinatario.id,
            "rut_destinatario": destinatario.rut_destinatario,
            "telefono": destinatario.telefono,
            "direccion": destinatario.direccion,
            "correo": destinatario.correo,
        }
    ), 200


@app.route("/paquetes/buscar", methods=["GET"])
def buscar_paquete():
    tipo = request.args.get("tipo")
    peso = request.args.get("peso")

    # Verificar errores de validación inicial
    errores_validacion = vde.buscar_paquete_error_get(tipo, peso)
    if errores_validacion:
        return jsonify(
            {"message": "Datos inválidos", "errores": errores_validacion}
        ), 400

    # Consultar la base de datos para encontrar el paquete
    paquete = vdd.Paquete.query.filter(
        (vdd.Paquete.tipo == tipo) & (vdd.Paquete.peso == peso)
    ).first()

    # Verificar errores después de la consulta
    errores_consulta = vde.buscar_paquete_error_get(tipo, peso, paquete)
    if errores_consulta:
        return jsonify(
            {"message": "Error al buscar el paquete", "errores": errores_consulta}
        ), 404

    # Si todo está bien, devolver la información del paquete
    return jsonify(
        {
            "id_paquete": paquete.id,
            "tipo": paquete.tipo,
            "peso": float(paquete.peso),
            "fecha_ingreso": paquete.fecha_ingreso,
        }
    ), 200


@app.route("/paquetes", methods=["POST"])
def create_paquete():
    data = request.get_json()

    errores = vde.paquete_error_post(data)
    if errores:
        return jsonify({"message": "Datos inválidos", "errores": errores}), 400

    tipo = data["tipo"]
    peso = data["peso"]

    nuevo_paquete = vdd.Paquete(tipo=tipo, peso=peso, fecha_ingreso=datetime.utcnow())
    db.session.add(nuevo_paquete)
    db.session.commit()

    return jsonify(
        {"message": "Nuevo paquete creado", "id_paquete": nuevo_paquete.id}
    ), 201


@app.route("/paquetes/<int:id_paquete>", methods=["GET"])
def get_paquete(id_paquete):
    paquete = vdd.Paquete.query.get_or_404(id_paquete)
    errores = vde.paquete_error_get(paquete)
    if errores:
        return jsonify(
            {"message": "Error al obtener el paquete", "errores": errores}
        ), 404

    return jsonify(
        {
            "id": paquete.id,
            "tipo": paquete.tipo,
            "peso": float(paquete.peso),  # Convertir Decimal a float
            "fecha_ingreso": paquete.fecha_ingreso.isoformat(),
        }
    )


@app.route("/envios", methods=["POST"])
def create_envio():
    data = request.get_json()

    required_fields = [
        "codigo_postal",
        "tipo_envio",
        "pagado",
        "recogida_a_domicilio",
        "reparto_a_domicilio",
        "por_pagar",
        "id_paquete",
        "id_remitente",
        "id_destinatario",
    ]
    errores = vde.check_required_fields(data, required_fields)
    if errores:
        return jsonify({"message": "Datos inválidos", "errores": errores}), 400

    errores += vde.check_tipo_envio(data)
    if errores:
        return jsonify({"message": "Datos inválidos", "errores": errores}), 400

    integer_fields = ["id_paquete", "id_remitente", "id_destinatario"]
    errores += vde.check_integer_fields(data, integer_fields)
    if errores:
        return jsonify({"message": "Datos inválidos", "errores": errores}), 400

    boolean_fields = ["pagado", "recogida_a_domicilio", "por_pagar", "reparto_a_domicilio"]
    errores += vde.check_boolean_fields(data, boolean_fields)
    if errores:
        return jsonify({"message": "Datos inválidos", "errores": errores}), 400

    nuevo_envio = vdd.Envio(
        codigo_postal=data["codigo_postal"],
        tipo_envio=data["tipo_envio"],
        pagado=data["pagado"],
        recogida_a_domicilio=data["recogida_a_domicilio"],
        reparto_a_domicilio=data["reparto_a_domicilio"],
        por_pagar=data["por_pagar"],
        id_paquete=data["id_paquete"],
        id_remitente=data["id_remitente"],
        id_destinatario=data["id_destinatario"],
        estado="en preparación",
        fecha_recepcion=datetime.utcnow(),
    )
    db.session.add(nuevo_envio)
    db.session.commit()

    return jsonify({"message": "Nuevo envío creado", "id_envio": nuevo_envio.id}), 201


@app.route("/envios/<int:envio_id>", methods=["GET"])
def get_envio_by_id(envio_id):
    try:
        envio = vdd.Envio.query.get(envio_id)

        paquete = vdd.Paquete.query.get(envio.id_paquete)
        remitente = vdd.Remitente.query.get(envio.id_remitente)
        destinatario = vdd.Destinatario.query.get(envio.id_destinatario)
        nombre_remitente = vdd.Cliente.query.get(remitente.rut_remitente)
        nombre_destinatario = vdd.Cliente.query.get(destinatario.rut_destinatario)

        resultado = {
            "id_envio": envio.id,
            "estado": envio.estado,
            "recogida_a_domicilio": envio.recogida_a_domicilio,
            "por_pagar": envio.por_pagar,
            "tipo_envio": envio.tipo_envio,
            "codigo_postal": envio.codigo_postal,
            "fecha_recepcion": envio.fecha_recepcion.isoformat()
            if envio.fecha_recepcion
            else None,
            "reparto_a_domicilio": envio.reparto_a_domicilio
            if envio.reparto_a_domicilio
            else None,
            "pagado": envio.pagado,
            "paquete": {
                "id_paquete": paquete.id,
                "tipo": paquete.tipo,
                "peso": float(paquete.peso) if paquete.peso else None,
                "fecha_ingreso": paquete.fecha_ingreso.isoformat()
                if paquete.fecha_ingreso
                else None,
            },
            "remitente": {
                "id_remitente": remitente.id,
                "rut_remitente": remitente.rut_remitente,
                "nombre": nombre_remitente.nombre if nombre_remitente else None,
                "direccion": remitente.direccion,
                "correo": remitente.correo,
            },
            "destinatario": {
                "id_destinatario": destinatario.id,
                "rut_destinatario": destinatario.rut_destinatario,
                "nombre": nombre_destinatario.nombre if nombre_destinatario else None,
                "telefono": destinatario.telefono,
                "direccion": destinatario.direccion,
                "correo": destinatario.correo,
            },
        }
        return jsonify(resultado)
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/envios/por_pagar", methods=["GET"])
def get_envios_por_pagar():
    try:
        envios_por_pagar = vdd.Envio.query.filter_by(por_pagar=True).all()

        resultados = []
        for envio in envios_por_pagar:
            paquete = vdd.Paquete.query.get(envio.id_paquete)
            remitente = vdd.Remitente.query.get(envio.id_remitente)
            destinatario = vdd.Destinatario.query.get(envio.id_destinatario)
            nombre_remitente = vdd.Cliente.query.get(remitente.rut_remitente)
            nombre_destinatario = vdd.Cliente.query.get(destinatario.rut_destinatario)

            resultados.append(
                {
                    "id_envio": envio.id,
                    "estado": envio.estado,
                    "recogida_a_domicilio": envio.recogida_a_domicilio,
                    "por_pagar": envio.por_pagar,
                    "tipo_envio": envio.tipo_envio,
                    "codigo_postal": envio.codigo_postal,
                    "fecha_recepcion": envio.fecha_recepcion.isoformat()
                    if envio.fecha_recepcion
                    else None,
                    "reparto_a_domicilio": envio.reparto_a_domicilio
                    if envio.reparto_a_domicilio
                    else None,
                    "pagado": envio.pagado,
                    "paquete": {
                        "id_paquete": paquete.id,
                        "tipo": paquete.tipo,
                        "peso": float(paquete.peso) if paquete.peso else None,
                        "fecha_ingreso": paquete.fecha_ingreso.isoformat()
                        if paquete.fecha_ingreso
                        else None,
                    },
                    "remitente": {
                        "id_remitente": remitente.id,
                        "rut_remitente": remitente.rut_remitente,
                        "nombre": nombre_remitente.nombre if nombre_remitente else None,
                        "direccion": remitente.direccion,
                        "correo": remitente.correo,
                    },
                    "destinatario": {
                        "id_destinatario": destinatario.id,
                        "rut_destinatario": destinatario.rut_destinatario,
                        "nombre": nombre_destinatario.nombre
                        if nombre_destinatario
                        else None,
                        "telefono": destinatario.telefono,
                        "direccion": destinatario.direccion,
                        "correo": destinatario.correo,
                    },
                }
            )
        return jsonify(resultados)
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/historial', methods=['POST'])
def crear_historial():
    data = request.get_json()
    try:
        # Obtener todos los historiales existentes para el id_envio
        historiales = vdd.Historial.query.filter_by(id_envio=data['id_envio']).all()
        
        # Verificar si ya hay un estado "entregado"
        for historial in historiales:
            if "entregado" in historial.estado:
                return jsonify({"error": "El envío ya fue entregado"}), 400
        
                
        fecha_mod = datetime.strptime(data['fecha_mod'], '%Y-%m-%dT%H:%M:%S.%fZ')
        nuevo_historial = vdd.Historial(
            fecha_mod=fecha_mod,
            estado=data['estado'],
            id_envio=data['id_envio']
        )
        db.session.add(nuevo_historial)
        db.session.commit()
        return jsonify({"mensaje": "Historial creado con éxito"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route("/historial/<int:id_envio>", methods=["GET"])
def obtener_historial(id_envio):
    try:
        historiales = vdd.Historial.query.filter_by(id_envio=id_envio).all()
        if not historiales:
            return jsonify({"mensaje": "No se encontraron historiales para el id_envio proporcionado"}), 404
        
        result = [
            {
                "id": h.id,
                "fecha_mod": h.fecha_mod.strftime('%Y-%m-%d %H:%M:%S'),
                "estado": h.estado,
                "id_envio": h.id_envio
            }
            for h in historiales
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/calcular_precio/<int:id_envio>', methods=['GET'])
def calcular_precio(id_envio):
    try:
        TARIFAS = Parametros(10000, 7000, 5000, 1500, 2000, Decimal('0.19'))
        envio = vdd.Envio.query.get(id_envio)
        listaPrecios = {}

        if not envio:
            return jsonify({"error": "Envío no encontrado"}), 404
        
        paquete = vdd.Paquete.query.get(envio.id_paquete)
        
        if not paquete:
            return jsonify({"error": "Paquete no encontrado"}), 404

        tipo_envio = envio.tipo_envio
        tipo_paquete = paquete.tipo
        peso_paquete = paquete.peso
        recogida_a_domicilio = envio.recogida_a_domicilio
        reparto_a_domicilio = envio.reparto_a_domicilio

        precio = Decimal('0')

        # Calcular tarifa base según el tipo de envío y tipo de paquete
        if tipo_paquete == 'sobre':
            precio += Decimal(TARIFAS.tarifas['sobre'][tipo_envio])
            listaPrecios['precio_por_tipo_de_envio'] = TARIFAS.tarifas['sobre'][tipo_envio]
        elif tipo_paquete == 'encomienda' and peso_paquete:
            precio += Decimal(TARIFAS.tarifas['encomienda'][tipo_envio]) * peso_paquete
            listaPrecios['precio_por_tipo_de_envio'] = TARIFAS.tarifas['encomienda'][tipo_envio] * peso_paquete
        else:
            return jsonify({"error": "Información del envío incompleta"}), 400

        # Agregar costo de entrega a domicilio si aplica
        if reparto_a_domicilio:
            precio += Decimal(TARIFAS.entrega_domicilio)
            listaPrecios['precio_por_reparto_a_domicilio'] = TARIFAS.entrega_domicilio

        # Agregar costo de recogida a domicilio si aplica
        if recogida_a_domicilio:
            precio += Decimal(TARIFAS.recogida_domicilio)
            listaPrecios['precio_por_recogida_a_domicilio'] = TARIFAS.recogida_domicilio
        
        # Calcular total incluyendo IVA
        total_con_iva = precio * (Decimal('1') + TARIFAS.iva)
        listaPrecios['total_con_IVA'] = total_con_iva

        return jsonify({"precios_detallados": listaPrecios}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400