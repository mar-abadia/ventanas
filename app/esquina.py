class Esquina:
    
    def __init__(self, precio_unitario=4310):
        self.precio_unitario = precio_unitario

class Chapa:
    def __init__(self, estilo_ventana, precio_chapa=16200):
        self.estilo_ventana = estilo_ventana
        self.precio_chapa = precio_chapa if "X" in estilo_ventana else 0