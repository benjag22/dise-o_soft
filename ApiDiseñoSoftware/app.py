from database import db, app
import controladorDeDatos as cdd

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)