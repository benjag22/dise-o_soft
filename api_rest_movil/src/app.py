from email.mime.multipart import MIMEMultipart
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:.@localhost:5432/envios'

# Crear la instancia de SQLAlchemy y asociarla con la aplicación Flask
db = SQLAlchemy(app)


# Definición del modelo Envio
class Envio(db.Model):
    __tablename__ = 'envios'

    id = db.Column(db.Integer, primary_key=True)
    remitente = db.Column(db.String(50))
    destinatario = db.Column(db.String(50))
    fono = db.Column(db.String(50))
    direccionEnvio = db.Column(db.String(120))
    ciudad = db.Column(db.String(50))
    tipoEnvio = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    porPagar = db.Column(db.Boolean)
    fechaRecepcion = db.Column(db.String(50))
    codigoPostal = db.Column(db.String(50))
    esSobre = db.Column(db.Boolean)
    peso = db.Column(db.Float)
    recogidaADomicilio = db.Column(db.Boolean)
    direccionRemitente = db.Column(db.String(120))
    repartoADomicilio = db.Column(db.Boolean)
    rutDestinatario = db.Column(db.String(10))
    pagado = db.Column(db.Boolean, default=False)
    entregado = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()   

     
def ping():
    return jsonify({'status': 'ok'})


def obtener_estado_solicitud_desde_bd(id, rut):
    envio = Envio.query.filter_by(id=id, rutDestinatario=rut).first()
    if envio:
        return True
    else:
        return False

def obtener_rut_desde_url(url):
    patron = r"RUN=([0-9]+-[0-9Kk])"
    match = re.search(patron, url)
    if match:
        return match.group(1)
    else:
        return None

def validar_rut(id, rut, url):
    rut_url = obtener_rut_desde_url(url)
    if rut_url == rut:
        estado = obtener_estado_solicitud_desde_bd(id, rut)
        if estado:
            return jsonify({'estado_solicitud': estado}), 200
        else:
            return jsonify({'error': 'RUT no válido para verificación'}), 400
    else:
        return jsonify({'error': 'RUT del URL no coincide con el RUT proporcionado'}), 400

@app.route("/verificar_rut/<int:id>/<string:rut>", methods=["GET"])
def verificarRut(id, rut):
    return validar_rut(id, rut, "https://portal.sidiv.registrocivil.cl/usuarios-portal/pages/DocumentRequestStatus.xhtml?RUN=21390811-1&type=CEDULA&serial=529885698")


@app.route("/envios/por_pagar", methods=["GET"])
def obtener_primer_envio_por_pagar():
    envios = Envio.query.filter_by(porPagar=True).all()
    envios_list = []
    for envio in envios:
        envio_dict = envio.__dict__
        del envio_dict["_sa_instance_state"]
        envios_list.append(envio_dict)
    return jsonify(envios_list)

def enviarCorreo(correo, id, destinatario):
    user = "benjagonzalez2022@inf.udec.cl"
    passw = "marfbgodlybswhhb"
    destinatario_correo = correo
    asunto = "Pedido"+  str(id)
    mensaje = "Estimado/a cliente,\n\nSu envio con el ID " + str(id) + " dirigido a "+ destinatario +", a sido entregado correctamente.\n\nGracias por su preferencia"
    
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = destinatario_correo
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user, passw)
        text = msg.as_string()
        server.sendmail(user, destinatario_correo, text)
        print("Correo enviado correctamente")
        server.quit()
    except Exception as e:
        print("0")


@app.route("/entregarEnvio/<int:id>/<string:correo>/<string:destinatario>", methods=["PATCH"])
def modificarEnvio(id, correo, destinatario):
    data = request.json

    envio = Envio.query.get(id)
    if envio:
        if 'entregado' in data:
            envio.entregado = data['entregado']
        db.session.commit()
        enviarCorreo(correo, id, destinatario)
        return jsonify({"message": "Envío modificado y correo enviado correctamente"}), 200
    else:
        return jsonify({"error": "Envío no encontrado"}), 404

@app.route("/detalle_envio/<int:id>", methods=["GET"])
def detalles_envio(id):
    envio = Envio.query.filter_by(id=id).first()
    if envio is None:
        return jsonify({"error": "Envio no encontrado"}), 404

    envio_data = {
        "id": envio.id,
        "remitente": envio.remitente,
        "destinatario": envio.destinatario,
        "fono": envio.fono,
        "direccionEnvio": envio.direccionEnvio,
        "ciudad": envio.ciudad,
        "tipoEnvio": envio.tipoEnvio,
        "correo": envio.correo,
        "porPagar": envio.porPagar,
        "fechaRecepcion": envio.fechaRecepcion,
        "codigoPostal": envio.codigoPostal,
        "esSobre": envio.esSobre,
        "peso": envio.peso,
        "recogidaADomicilio": envio.recogidaADomicilio,
        "direccionRemitente": envio.direccionRemitente,
        "repartoADomicilio": envio.repartoADomicilio,
        "rutDestinatario": envio.rutDestinatario,
        "pagado": envio.pagado,
        "entregado": envio.entregado
    }
    return jsonify(envio_data)

if __name__ == '__main__':
    app.run(debug=True, port=4000)
