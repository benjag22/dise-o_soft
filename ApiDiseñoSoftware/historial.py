from datetime import datetime

class Historial:
    estados_posibles = ["en preparación", "en tránsito", "en sucursal", "en reparto", "entregado"]
    
    def __init__(self, id_envio, fecha_mod, estado):
        self.id_envio = id_envio
        self.fecha_mod = fecha_mod
        self.estado = estado

    def getEstado(self):
        return self.estado