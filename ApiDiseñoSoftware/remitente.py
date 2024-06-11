from cliente import Cliente

class Remitente(Cliente):
    def __init__(self, rut, nombre, direccion, correo):
        super().__init__(rut, nombre, direccion)
        self.correo = correo

    def get_correo(self):
        return self.correo