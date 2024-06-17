class Parametros:
    def __init__(self, tarifa_dia, tarifa_rapida, tarifa_normal, entrega_domicilio, recogida_domicilio,IVA):
        self.tarifas = {
            'sobre': {
                'entrega en el día': tarifa_dia,
                'entrega rápida': tarifa_rapida,
                'entrega normal': tarifa_normal
            },
            'encomienda': {
                'entrega en el día': tarifa_dia,  # $/kg
                'entrega rápida': tarifa_rapida,  # $/kg
                'entrega normal': tarifa_normal   # $/kg
            }
        }
        self.entrega_domicilio = entrega_domicilio
        self.recogida_domicilio = recogida_domicilio
        self.iva=IVA
