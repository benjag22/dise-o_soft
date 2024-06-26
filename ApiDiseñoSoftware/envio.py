from datetime import datetime
from historial import Historial
from datetime import datetime
from decimal import Decimal
from paquete import Paquete
from destinatario import Destinatario
from remitente import Remitente
from pago import Pago
from cliente import Cliente

class Envio:
    estados_posibles = ["en preparación", "en tránsito", "en sucursal", "en reparto", "entregado"]

    def __init__(self, id_envio, cod_postal, tipo_envio, recogida_a_domicilio, reparto_a_domicilio, paquete, remitente, destinatario): 
        self.id_envio = id_envio
        self.cod_postal = cod_postal
        self.tipo_envio = tipo_envio
        self.recogida_a_domicilio = recogida_a_domicilio
        self.reparto_a_domicilio = reparto_a_domicilio
        self.paquete = Paquete(paquete.tipo, paquete.peso)
        self.remitente = Remitente(remitente.rut, remitente.nombre, remitente.direccion,remitente.correo)
        self.destinatario = Destinatario(destinatario.rut, destinatario.nombre, destinatario.direccion, destinatario.telefono)
        self.fecha_recepcion = datetime.utcnow()
        self.historial = []
        self.pagos = []

    def getId(self):
        return self.id_envio
    def get_cod_postal(self):
        return self.cod_postal

    def get_tipo_envio(self):
        return self.tipo_envio

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



    def siguienteEstado(self, nuevo_estado, fecha_mod):
        if nuevo_estado not in self.estados_posibles:
            raise ValueError("Estado no válido.")

        ultimo_estado = self.historial[-1].estado if self.historial else self.estado
        if self.estados_posibles.index(nuevo_estado) <= self.estados_posibles.index(ultimo_estado):
            raise ValueError("Transición de estado inválida.")

        self.estado = Historial(self.id_envio, fecha_mod, nuevo_estado)
        self.historial.append(self.estado)
        return self.estado
    
    def siguienteEstado(self):
        if not self.historial:
            ultimo_estado = self.estados_posibles[0]
        else:
            ultimo_estado = self.get_last_historial()

        try:
            nuevo_estado = self.estados_posibles[self.estados_posibles.index(ultimo_estado) + 1]
        except IndexError:
            raise ValueError("No hay estados siguientes disponibles. El envío ya está en el estado final.")

        self.historial.append({"estado": nuevo_estado, "fecha": datetime.utcnow()})
        return self.historial[-1]
    

    def valor_por_envio(self, parametros, cliente: Cliente, pagado):
        precio = Decimal('0')
        lista_precios = {}

        tipo_paquete = self.paquete['tipo']
        tipo_envio = self.tipo_envio
        peso_paquete = self.paquete.get('peso', 0)

        # Calcular tarifa base según el tipo de envío y tipo de paquete
        if tipo_paquete == 'sobre':
            precio += parametros.precioPaquete(tipo_paquete, tipo_envio)
            lista_precios['precio_por_tipo_de_envio'] = parametros.get_tarifa(tipo_paquete, tipo_envio)
        elif tipo_paquete == 'encomienda' and peso_paquete:
            precio += parametros.precioPaquete(tipo_paquete, tipo_envio) * Decimal(peso_paquete)
            lista_precios['precio_por_tipo_de_envio'] = parametros.get_tarifa(tipo_paquete, tipo_envio) * Decimal(peso_paquete)
        else:
            raise ValueError("Información del envío incompleta o incorrecta")

        # Agregar costo de entrega a domicilio si aplica
        if self.reparto_a_domicilio:
            precio += parametros.precioRepartoDomicilio()
            lista_precios['precio_por_reparto_a_domicilio'] = parametros.get_entrega_domicilio()

        # Agregar costo de recogida a domicilio si aplica
        if self.recogida_a_domicilio:
            precio += parametros.precioRecogidaDomicilio()
            lista_precios['precio_por_recogida_a_domicilio'] = parametros.get_recogida_domicilio()

        # Calcular total incluyendo IVA
        total_con_iva = precio * (Decimal('1') + parametros.IVA())
        lista_precios['total_con_IVA'] = total_con_iva

        pago = Pago(pagado, total_con_iva, cliente)
        self.pagos.append(pago)

        return lista_precios
    
    
    def mostrar_historial(self):
        return [hist.to_dict() for hist in self.historial]
    
    def get_last_historial(self):
        if not self.historial:
            return None  
        return self.historial[-1]

    