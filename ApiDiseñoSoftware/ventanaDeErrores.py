import validadorDeDatos as vdd

def clientes_error_post(data):
    errores = []
    if not data:
        errores.append('No se proporcionaron datos.')
    else:
        if 'rut' not in data:
            errores.append('Falta el campo "rut".')
        if 'nombre' not in data:
            errores.append('Falta el campo "nombre".')
        if 'ap_paterno' not in data:
            errores.append('Falta el campo "ap_paterno".')
        if 'ap_materno' not in data:
            errores.append('Falta el campo "ap_materno".')
        if 'estado' not in data:
            errores.append('Falta el campo "estado".')
    return errores

def cliente_error_get(rut):
    errores = []
    if not rut:
        errores.append('No se proporcionó el RUT.')
    else:
        cliente = vdd.Cliente.query.filter_by(rut=rut).first()
        if not cliente:
            errores.append('No se encontró el cliente con el RUT proporcionado.')
    return errores

def remitentes_error_post(data):
    errores = []
    if not data:
        errores.append('No se proporcionaron datos.')
    else:
        if 'rut_remitente' not in data:
            errores.append('Falta el campo "rut_remitente".')
        if 'correo' not in data:
            errores.append('Falta el campo "correo".')
        if 'direccion' not in data:
            errores.append('Falta el campo "direccion".')
    return errores


def remitente_error_get(remitente):
    errores = []
    if not remitente:
        errores.append('No se encontró el remitente.')
    return errores

def buscar_remitente_error_get(rut, direccion, correo):
    errores = []
    if not rut:
        errores.append('Falta el parámetro "rut" en la solicitud.')
    if not direccion:
        errores.append('Falta el parámetro "direccion" en la solicitud.')
    if not correo:
        errores.append('Falta el parámetro "correo" en la solicitud.')
    return errores

def destinatario_error_post(data):
    errores = []

    if not data:
        errores.append('No se proporcionaron datos.')
    else:
        if 'rut_destinatario' not in data:
            errores.append('Falta el campo "rut_destinatario".')
        if 'telefono' not in data:
            errores.append('Falta el campo "telefono".')
        if 'direccion' not in data:
            errores.append('Falta el campo "direccion".')
        if 'correo' not in data:
            errores.append('Falta el campo "correo".')

    return errores

def destinatario_error_get(destinatario):
    errores = []
    if not destinatario:
        errores.append('No se encontró el destinatario.')
    return errores

def destinatario_error_buscar(rut, direccion, telefono, destinatario):
    errores = []
    if not rut or not direccion or not telefono:
        errores.append('Faltan datos: se requieren rut, dirección y teléfono.')
    if not destinatario:
        errores.append('No se encontró ningún destinatario con los datos proporcionados.')
    return errores

def paquete_error_get(tipo, peso, paquete):
    errores = []

    if not tipo:
        errores.append('Falta el parámetro "tipo".')
    if not peso:
        errores.append('Falta el parámetro "peso".')
    if not paquete:
        errores.append('No se encontró ningún paquete con esos datos.')

    return errores