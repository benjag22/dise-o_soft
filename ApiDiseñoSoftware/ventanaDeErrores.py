import validadorDeDatos as vdd
import datetime 
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

def buscar_paquete_error_get(tipo, peso):
    errores = []

    # Verificar 'tipo'
    valid_tipos = ['sobre', 'encomienda']
    if tipo and tipo not in valid_tipos:
        errores.append({'campo': 'tipo', 'mensaje': 'Tipo inválido. Debe ser "sobre" o "encomienda".'})

    # Verificar 'peso'
    if peso:
        try:
            peso_float = float(peso)
            if peso_float < 0:
                errores.append({'campo': 'peso', 'mensaje': 'El peso debe ser un número positivo.'})
        except ValueError:
            errores.append({'campo': 'peso', 'mensaje': 'El peso debe ser un número válido.'})

    return errores


def paquete_error_post(data):
    errores = []

    # Verificar 'tipo'
    valid_tipos = ['sobre', 'encomienda']
    if 'tipo' not in data or data['tipo'] not in valid_tipos:
        errores.append({'campo': 'tipo', 'mensaje': 'Tipo inválido. Debe ser "sobre" o "encomienda".'})

    # Verificar 'peso'
    if 'peso' not in data:
        errores.append({'campo': 'peso', 'mensaje': 'El peso es requerido.'})
    else:
        try:
            peso = float(data['peso'])
            if peso < 0:
                errores.append({'campo': 'peso', 'mensaje': 'El peso debe ser un número positivo.'})
        except ValueError:
            errores.append({'campo': 'peso', 'mensaje': 'El peso debe ser un número válido.'})

    # Verificar 'fecha_ingreso' si está presente
    if 'fecha_ingreso' in data:
        try:
            datetime.fromisoformat(data['fecha_ingreso'])
        except ValueError:
            errores.append({'campo': 'fecha_ingreso', 'mensaje': 'Fecha de ingreso inválida.'})

    return errores

def check_required_fields(data, required_fields):
    errores = []
    for field in required_fields:
        if field not in data:
            errores.append({'campo': field, 'mensaje': f'El campo {field} es requerido.'})
    return errores

def check_tipo_envio(data):
    errores = []
    valid_tipos_envio = ['entrega en el día', 'entrega rápida', 'entrega normal']
    if 'tipo_envio' in data and data['tipo_envio'] not in valid_tipos_envio:
        errores.append({'campo': 'tipo_envio', 'mensaje': 'Tipo de envío inválido. Debe ser "entrega en el día", "entrega rápida" o "entrega normal".'})
    return errores

def check_integer_fields(data, integer_fields):
    errores = []
    for field in integer_fields:
        if field in data:
            try:
                int(data[field])
            except ValueError:
                errores.append({'campo': field, 'mensaje': f'El campo {field} debe ser un entero válido.'})
    return errores


def check_boolean_fields(data, boolean_fields):
    errores = []
    for field in boolean_fields:
        if field in data and not isinstance(data[field], bool):
            errores.append({'campo': field, 'mensaje': f'El campo {field} debe ser booleano.'})
    return errores




    