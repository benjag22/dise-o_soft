from cliente import Cliente
from remitente import Remitente
from destinatario import Destinatario
from paquete import Paquete
from envio import Envio
from parametros import Parametros

def main():
    cliente1 = Cliente("12345678-9", "Juan")
    cliente2 = Cliente("98765432-1", "Pedro")

    remitente = Remitente(cliente1.get_rut(), cliente1.get_nombre(), "Angol 123", "hola@gmail.com")
    destinatario = Destinatario(cliente2.get_rut(), cliente2.get_nombre(), "prat 24314", "962291615")
    paquete = Paquete("encomienda", 1.2)

    envio = Envio("12345", "Entrega rápida", True, True, False, False, paquete, remitente, destinatario)

    envio.actualizar_estado("En tránsito")
    envio.actualizar_estado("En sucursal")
    envio.actualizar_estado("En reparto")
    envio.actualizar_estado("Entregado")

    print("Nuevo estado del Envío:", envio.get_estado())
    envio.mostrar_historial()

    parametros = Parametros(5000, 3000, 0.19, 1000, 2000)

if __name__ == "__main__":
    main()
