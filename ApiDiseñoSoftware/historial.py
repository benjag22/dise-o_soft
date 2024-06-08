class Historial:
    def __init__(self, envio, fecha_mod):
        self.envio = envio
        self.fecha_mod = fecha_mod

    def get_envio(self):
        return self.envio

    def get_fecha_mod(self):
        return self.fecha_mod
