# app.py
from flask import Flask
from flask_cors import CORS
from database import db
from ClienteAPI import ClienteAPI
from DestinatarioAPI import DestinatarioAPI
from RemitenteAPI import RemitenteAPI
from PaqueteAPI import PaqueteAPI
from EnvioAPI import EnvioAPI
from HistorialAPI import HistorialAPI

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:.@localhost:5432/envios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

    cliente_api = ClienteAPI(db) 
    app.register_blueprint(cliente_api.bp, url_prefix='/api')

    destinatario_api = DestinatarioAPI(db)
    app.register_blueprint(destinatario_api.bp, url_prefix='/api')

    remitente_api=RemitenteAPI(db)
    app.register_blueprint(remitente_api.bp, url_prefix='/api')

    paquete_api = PaqueteAPI(db)
    app.register_blueprint(paquete_api.bp, url_prefix='/api')
    
    envio_api = EnvioAPI(db)
    app.register_blueprint(envio_api.bp, url_prefix='/api')

    historial_api= HistorialAPI(db)
    app.register_blueprint(historial_api.bp, url_prefix='/api')
    

    app.run(debug=True, port=5000)