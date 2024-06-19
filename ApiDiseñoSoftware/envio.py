from datetime import datetime
from historial import Historial
from datetime import datetime

class Envio:
    estados_posibles = ["en preparación", "en tránsito", "en sucursal", "en reparto", "entregado"]

    def __init__(self, id_envio, cod_postal, tipo_envio, pagado, recogida_a_domicilio, reparto_a_domicilio, por_pagar, paquete, remitente, destinatario, estado="en preparación"):
        self.id_envio = id_envio
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

    def getId(self):
        return self.id_envio
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

    def actualizar_estado(self, nuevo_estado, fecha_mod):
        if nuevo_estado not in self.estados_posibles:
            raise ValueError("Estado no válido.")

        ultimo_estado = self.historial[-1].estado if self.historial else self.estado
        if self.estados_posibles.index(nuevo_estado) <= self.estados_posibles.index(ultimo_estado):
            raise ValueError("Transición de estado inválida.")

        historial = Historial(self.id_envio, fecha_mod, nuevo_estado)
        self.historial.append(historial)
        return historial

    def mostrar_historial(self):
        return [hist.to_dict() for hist in self.historial]