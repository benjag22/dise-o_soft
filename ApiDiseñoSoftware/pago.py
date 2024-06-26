from cliente import Cliente
from formaPago import FormaPago

class Pago:

    def __init__(self,formaDePago,valorEnvio,cliente):
        self.formaDePago = formaDePago
        self.valorEnvio = valorEnvio
        self.cliente: Cliente = cliente
        self.pagado = False
        if formaDePago == FormaPago.pagado:
            self.enviar_pago()

    def enviar_pago(self):
        #Aqui se lanzaria el pago en Verificacion de pago
        pagoExitoso = True
        if pagoExitoso:
            self.pagado = True
        return pagoExitoso
    
    def get_pagado(self):
        return self.pagado