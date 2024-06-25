from cliente import Cliente

class Pago:

    def __init__(self,formaDePago,valorEnvio,cliente):
        self.formaDePago = formaDePago
        self.valorEnvio = valorEnvio
        self.cliente = cliente

    def enviar_pago(self):
        return [self.formaDePago,self.valorEnvio,self.cliente]