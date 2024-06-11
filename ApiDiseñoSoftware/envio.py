from datetime import datetime
from historial import Historial
class Envio:
    def __init__(self, cod_postal, tipo_envio, pagado, recogida_a_domicilio, reparto_a_domicilio, por_pagar, paquete, remitente, destinatario,estado="En preparación"):
        self.cod_postal = cod_postal
        self.tipo_envio = tipo_envio
        self.pagado = pagado
        self.recogida_a_domicilio = recogida_a_domicilio
        self.reparto_a_domicilio = reparto_a_domicilio
        self.por_pagar = por_pagar
        self.paquete = paquete
        self.remitente = remitente
        self.destinatario = destinatario
        self.fecha_recepcion = datetime.utcnow()
        self.estado = estado
        self.historial = []
        self.estados_posibles = ["En preparación", "En tránsito", "En sucursal", "En reparto", "Entregado"]
    def get_cod_postal(self):
        return self.cod_postal

    def get_tipo_envio(self):
        return self.tipo_envio

    def get_pagado(self):
        return self.pagado

    def get_recogida_a_domicilio(self):
        return self.recogida_a_domicilio

    def get_reparto_a_domicilio(self):
        return self.reparto_a_domicilio

    def get_por_pagar(self):
        return self.por_pagar

    def get_paquete(self):
        return self.paquete

    def get_remitente(self):
        return self.remitente

    def get_destinatario(self):
        return self.destinatario

    def get_fecha_recepcion(self):
        return self.fecha_recepcion

    def get_estado(self):
        return self.estado

    def actualizar_estado(self, nuevo_estado):
        if nuevo_estado in self.estados_posibles:
            self.estado = nuevo_estado
            self.registrar_historial(nuevo_estado)
        else:
            print("Estado no válido.")

    def registrar_historial(self, estado):
        self.historial.append((estado, datetime.now()))

    def mostrar_historial(self):
        for estado, fecha in self.historial:
            print("Estado:", estado, "Fecha:", fecha.strftime("%Y-%m-%d %H:%M:%S"))