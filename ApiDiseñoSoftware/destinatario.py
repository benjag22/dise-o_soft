from cliente import Cliente

class Destinatario(Cliente):
    def __init__(self, rut, nombre, direccion, telefono):
        super().__init__(rut, nombre, direccion)
        self.telefono = telefono

    def get_telefono(self):
        return self.telefono
