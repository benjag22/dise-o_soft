from cliente import Cliente

class Pago:

    def __init__(self,valorEnvio,cliente):
        self.valorEnvio = valorEnvio
        self.cliente: Cliente = cliente
        self.pagado = False
        self.pago_cancelado = False

    def enviar_pago(self):
        if self.pago_cancelado:
            return False
        #Aqui se lanzaria el pago en Verificacion de pago, simulando la verificacion de pago 
        pagoExitoso = True
        if pagoExitoso:
            self.pagado = True
        return pagoExitoso
    
    def get_pagado(self):
        return self.pagado
    
    def setPago_cancelado(self):
        self.pago_cancelado = True