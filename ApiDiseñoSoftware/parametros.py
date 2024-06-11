class Parametros:
    def __init__(self, precio_encomienda, precio_sobre, IVA, precio_por_kg, monto_recogida_domicilio):
        self.precio_encomienda = precio_encomienda
        self.precio_sobre = precio_sobre
        self.IVA = IVA
        self.precio_por_kg = precio_por_kg
        self.monto_recogida_domicilio = monto_recogida_domicilio

    def get_precio_encomienda(self):
        return self.precio_encomienda

    def get_precio_sobre(self):
        return self.precio_sobre

    def get_IVA(self):
        return self.IVA

    def get_precio_por_kg(self):
        return self.precio_por_kg

    def get_monto_recogida_domicilio(self):
        return self.monto_recogida_domicilio
