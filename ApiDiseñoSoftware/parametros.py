from decimal import Decimal

class Parametros:
    def __init__(self, tarifa_dia, tarifa_rapida, tarifa_normal, entrega_domicilio, recogida_domicilio, IVA):
        self._tarifas = {
            'sobre': {
                'entrega en el día': Decimal(tarifa_dia),
                'entrega rápida': Decimal(tarifa_rapida),
                'entrega normal': Decimal(tarifa_normal)
            },
            'encomienda': {
                'entrega en el día': Decimal(tarifa_dia),  # $/kg
                'entrega rápida': Decimal(tarifa_rapida),  # $/kg
                'entrega normal': Decimal(tarifa_normal)   # $/kg
            }
        }
        self._entrega_domicilio = Decimal(entrega_domicilio)
        self._recogida_domicilio = Decimal(recogida_domicilio)
        self._iva = Decimal(IVA)

    def precioPaquete(self, tipo_paquete, tipo_envio):
        return self._tarifas[tipo_paquete][tipo_envio]

    def precioRepartoDomicilio(self):
        return self._entrega_domicilio

    def precioRecogidaDomicilio(self):
        return self._recogida_domicilio

    def IVA(self):
        return self._iva
