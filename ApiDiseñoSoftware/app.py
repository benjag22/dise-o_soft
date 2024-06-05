from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import false

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:.@localhost:5432/envios'

db = SQLAlchemy(app)

# Definición del modelo Envio
class Envio(db.Model):
    __tablename__ = 'envios'
    id = db.Column(db.Integer, primary_key=True)  #Listo
    remitente = db.Column(db.String(50))  # Listo
    destinatario = db.Column(db.String(50)) #listo
    fono = db.Column(db.String(50)) #listo
    direccionEnvio = db.Column(db.String(120)) #listo
    ciudad = db.Column(db.String(50)) # listo
    tipoEnvio = db.Column(db.String(50)) # listo
    correo = db.Column(db.String(50)) #listo
    porPagar = db.Column(db.Boolean) #listo
    fechaRecepcion = db.Column(db.String(50)) #listo
    codigoPostal = db.Column(db.String(50)) #listo
    esSobre = db.Column(db.Boolean) #listo
    peso = db.Column(db.Float) #listo
    recogidaADomicilio = db.Column(db.Boolean) #listo
    direccionRemitente = db.Column(db.String(120)) #listo
    repartoADomicilio = db.Column(db.Boolean) #listo
    rutDestinatario = db.Column(db.String(10)) #listo
    pagado = db.Column(db.Boolean, default=False) #listo
    entregado = db.Column(db.Boolean, default=False) #listo
    estado = db.Column(db.String(50), default='en preparación') # listo

with app.app_context():
    db.create_all()   

# Ruta para manejar el método POST desde el formulario React
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        data = request.json
        if data:
            envio = Envio(
                remitente=data.get('remitente'),
                destinatario=data.get('destinatario'),
                fono=data.get('fono'),
                direccionEnvio=data.get('direccionEnvio'),
                ciudad=data.get('ciudad'),
                tipoEnvio=data.get('tipoEnvio'),
                correo=data.get('correo'),
                porPagar=data.get('porPagar'),
                fechaRecepcion=data.get('fechaRecepcion'),
                codigoPostal=data.get('codigoPostal'),
                esSobre=data.get('esSobre'),
                peso=data.get('peso'),
                recogidaADomicilio=data.get('recogidaADomicilio'),
                direccionRemitente=data.get('direccionRemitente'),
                repartoADomicilio=data.get('repartoADomicilio'),
                rutDestinatario = data.get('rutDestinatario'),
                pagado = data.get('pagado'),
                entregado = data.get('entregado'),
                estado = data.get('entregado')
            )
            db.session.add(envio)
            db.session.commit()
            return jsonify({'message': 'Envío creado correctamente'}), 200
        else:
            return jsonify({'error': 'No se recibieron datos JSON'}), 400

    return jsonify({'error': 'Método no permitido'}), 405

@app.route("/")
def index():
    # Muestra una lista de envíos o algún otro contenido relacionado
    return render_template('index.html')
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)
