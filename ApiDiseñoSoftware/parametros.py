from decimal import Decimal
class Parametros:
    def __init__(self, tarifa_dia, tarifa_rapida, tarifa_normal, entrega_domicilio, recogida_domicilio, IVA):
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
        self.iva = IVA

    def calcular_tarifa_envio(self, tipo_paquete, tipo_envio, peso_paquete, recogida_a_domicilio, reparto_a_domicilio):
        precio = Decimal('0')
        listaPrecios = {}

        # Calcular tarifa base según el tipo de envío y tipo de paquete
        if tipo_paquete == 'sobre':
            precio += Decimal(self.tarifas['sobre'][tipo_envio])
            listaPrecios['precio_por_tipo_de_envio'] = self.tarifas['sobre'][tipo_envio]
        elif tipo_paquete == 'encomienda' and peso_paquete:
            precio += Decimal(self.tarifas['encomienda'][tipo_envio]) * peso_paquete
            listaPrecios['precio_por_tipo_de_envio'] = self.tarifas['encomienda'][tipo_envio] * peso_paquete
        else:
            raise ValueError("Información del envío incompleta o incorrecta")

        # Agregar costo de entrega a domicilio si aplica
        if reparto_a_domicilio:
            precio += Decimal(self.entrega_domicilio)
            listaPrecios['precio_por_reparto_a_domicilio'] = self.entrega_domicilio

        # Agregar costo de recogida a domicilio si aplica
        if recogida_a_domicilio:
            precio += Decimal(self.recogida_domicilio)
            listaPrecios['precio_por_recogida_a_domicilio'] = self.recogida_domicilio

        # Calcular total incluyendo IVA
        total_con_iva = precio * (Decimal('1') + self.iva)
        listaPrecios['total_con_IVA'] = total_con_iva

        return listaPrecios