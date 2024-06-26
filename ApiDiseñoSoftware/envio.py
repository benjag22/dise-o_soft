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
    estados_posibles = ["cancelado", "en preparación", "en tránsito", "en sucursal", "en reparto", "entregado"]


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
        self.pagado=False

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
    
    def siguienteEstado(self):
        ultimo_estado = self.get_last_historial()
        if ultimo_estado.getEstado() == "cancelado" or ultimo_estado.getEstado() == "entregado":
            return ultimo_estado
        
        nuevo_estado = self.estados_posibles[self.estados_posibles.index(ultimo_estado) + 1]

        self.historial.append({"estado": nuevo_estado, "fecha": datetime.utcnow()})
        return self.historial[-1]
    
        
    def cancelar_envio(self):
        estado_cancelado = Historial("cancelado",datetime.utcnow())
        self.historial.append(estado_cancelado)
        self.pago.setPago_cancelado()



    def get_last_historial(self):
        if not self.historial:
            return "en preparación"  
        return self.historial[-1]


    def crear_pago(self, parametros, cliente: Cliente):
        precio = Decimal('0')
        lista_precios = {}

        tipo_paquete = self.paquete.get_tipo()
        tipo_envio = self.tipo_envio
        peso_paquete = self.paquete.get_peso()

        # Calcular tarifa base según el tipo de envío y tipo de paquete
        tarifa = parametros.precioPaquete(tipo_paquete, tipo_envio)
        precio_paquete = tarifa

        if tipo_paquete == 'encomienda':
            precio_paquete *= Decimal(peso_paquete)
            tarifa *= Decimal(peso_paquete)

        precio += precio_paquete
        lista_precios['precio_por_tipo_de_envio'] = precio_paquete

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

        self.pago = Pago(total_con_iva, cliente)

        return lista_precios


    