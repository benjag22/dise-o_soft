class Cliente:
    def __init__(self, rut, nombre, direccion=None):
        self.rut = rut
        self.nombre = nombre
        self.direccion = direccion

    def get_rut(self):
        return self.rut

    def get_nombre(self):
        return self.nombre

    def get_direccion(self):
        return self.direccion