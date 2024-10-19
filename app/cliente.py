class Cliente:
    def __init__(self, nombre, empresa, cantidad_ventanas, direccion):
        self.nombre = nombre
        self.empresa = empresa
        self.cantidad_ventanas = cantidad_ventanas
        self.direccion = direccion  # Almacenar el nuevo parámetro

    def generar_reporte_cotizacion(self):
        reporte = f"Cotización para {self.cliente.nombre}\n"
        reporte += "Ventanas:\n"
        for ventana in self.ventanas:
            reporte += f"- Ventana {ventana.estilo}: {ventana.ancho}x{ventana.alto}, Costo Total: {ventana.calcular_costo_total()}\n"
        reporte += f"Total: {self.calcular_total()}"
        return reporte