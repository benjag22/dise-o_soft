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
    Remitente = db.Column(db.String(50))
    Destinatario = db.Column(db.String(50))
    Fono = db.Column(db.String(50))
    Direccion_envio = db.Column(db.String(120))
    Ciudad = db.Column(db.String(50))
    Tipo_de_envio = db.Column(db.String(50))
    Correo = db.Column(db.String(50))
    Por_pagar = db.Column(db.Boolean)
    Fecha_de_recepcion = db.Column(db.String(50))
    Codigo_postal = db.Column(db.String(50))
    Es_sobre = db.Column(db.Boolean)
    Peso = db.Column(db.Float)
    Recogida_a_domicilio = db.Column(db.Boolean)
    Direccion_remitente = db.Column(db.String(120))
    Reparto_a_domicilio = db.Column(db.Boolean)
    Rut_Destinatario = db.Column(db.String(10))
    pagado = db.Column(db.Boolean, default=False)
    entregado = db.Column(db.Boolean, default=False)
    

with app.app_context():
    db.create_all()  
     
def ping():
    return jsonify({'status': 'ok'})


def obtener_estado_solicitud_desde_bd(id, rut):
    envio = Envio.query.filter_by(id=id, Rut_Destinatario=rut).first()
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
    #url = request.url //para despues cuando sea global
    return validar_rut(id, rut, "https://portal.sidiv.registrocivil.cl/usuarios-portal/pages/DocumentRequestStatus.xhtml?RUN=21390811-1&type=CEDULA&serial=529885698")


@app.route("/envios/por_pagar", methods=["GET"])
def obtener_primer_envio_por_pagar():
    envios: list[Envio] = list(Envio.query.filter_by(Por_pagar=True).all())
    for i in range(len(envios)):
        json = envios[i].__dict__
        del json["_sa_instance_state"]
        envios[i] = json
    return jsonify(envios)

def enviarCorreo(Correo, id,Destinatario):
    user = "benjagonzalez2022@inf.udec.cl"
    passw = "marfbgodlybswhhb"
    destinatario = Correo
    asunto = "Pedido"+  str(id)
    mensaje = "Estimado/a cliente,\n\nSu envio con el ID " + str(id) + " dirigido a "+ Destinatario +", a sido entregado correctamente.\n\nGracias por su preferencia"
    
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user, passw)
        text = msg.as_string()
        server.sendmail(user, destinatario, text)
        print("1")
        server.quit()
    except Exception as e:
        print("0")


@app.route("/entregarEnvio/<int:id>/<string:Correo>/<string:Destinatario>", methods=["PATCH"])
def modificarEnvio(id, Correo, Destinatario):
    data = request.json

    envio = Envio.query.get(id)
    if envio:
        if 'entregado' in data:
            envio.entregado = data['entregado']
        db.session.commit()
        enviarCorreo(Correo, id, Destinatario)
        return jsonify({"message": "Envío modificado y correo enviado correctamente"}), 200
    else:
        return jsonify({"error": "Envío no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=4000)
