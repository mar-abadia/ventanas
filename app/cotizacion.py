class Cotizacion:
    def __init__(self, cliente, ventanas):
        self.cliente = cliente
        self.ventanas = ventanas

    def calcular_total(self):
        total = sum(ventana.calcular_costo_total() for ventana in self.ventanas)
        if self.cliente.cantidad_ventanas > 100:
            total *= 0.9  #  10% DESCUENTO
        return total
    
    def generar_reporte_cotizacion(self):
        reporte = f"Cotización para {self.cliente.nombre}\n"
        reporte += "Ventanas:\n"
        for ventana in self.ventanas:
            reporte += f"- Ventana {ventana.estilo}: {ventana.ancho}x{ventana.alto}, Costo Total: {ventana.calcular_costo_total()}\n"
        reporte += f"Total: {self.calcular_total()}"
        return reporte