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

# Ruta para manejar el método POST desde el formulario React
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        data = request.json
        if data:
            envio = Envio(
                Remitente=data.get('Remitente'),
                Destinatario=data.get('Destinatario'),
                Fono=data.get('Fono'),
                Direccion_envio=data.get('Direccion_envio'),
                Ciudad=data.get('Ciudad'),
                Tipo_de_envio=data.get('Tipo_de_envio'),
                Correo=data.get('Correo'),
                Por_pagar=data.get('Por_pagar'),
                Fecha_de_recepcion=data.get('Fecha_de_recepcion'),
                Codigo_postal=data.get('Codigo_postal'),
                Es_sobre=data.get('Es_sobre'),
                Peso=data.get('Peso'),
                Recogida_a_domicilio=data.get('Recogida_a_domicilio'),
                Direccion_remitente=data.get('Direccion_remitente'),
                Reparto_a_domicilio=data.get('Reparto_a_domicilio'),
                Rut_Destinatario = data.get('Rut_Destinatario'),
                pagado = data.get('pagado'),
                entregado = data.get('entregado')
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
