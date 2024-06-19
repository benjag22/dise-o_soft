from datetime import datetime

class Historial:
    def __init__(self, id_envio, fecha_mod, estado):
        self.id_envio = id_envio
        self.fecha_mod = fecha_mod
        self.estado = estado

    def to_dict(self):
        return {
            "id_envio": self.id_envio,
            "fecha_mod": self.fecha_mod.strftime('%Y-%m-%d %H:%M:%S'),
            "estado": self.estado
        }