from app.nave import Nave

class Ventana:
    def __init__(self, estilo, ancho, alto, acabado, tipo_vidrio, esmerilado=False):
        self.estilo = estilo  # O, XO, OXXO, OXO
        self.ancho = ancho
        self.alto = alto
        self.acabado = acabado  # Pulido, Lacado Brillante, etc.
        self.tipo_vidrio = tipo_vidrio  # Transparente, Bronce, Azul
        self.esmerilado = esmerilado
        self.naves = self.crear_naves()

    def calcular_ancho_naves(self):
        estilos_naves = {"O": 1, "XO": 2, "OXO": 3, "OXXO": 4}
        naves = estilos_naves[self.estilo]
        return self.ancho / naves, naves

    def crear_naves(self):
        ancho_nave, num_naves = self.calcular_ancho_naves()
        naves = [Nave(self.tipo_vidrio, ancho_nave, self.alto, self.acabado, self.esmerilado)
                 for _ in range(num_naves)]
        return naves

    def calcular_area_nave(self):
        ancho_nave, _ = self.calcular_ancho_naves()
        return (ancho_nave - 1.5) * (self.alto - 1.5)

    def calcular_perimetro_nave(self):
        ancho_nave, _ = self.calcular_ancho_naves()
        return 2 * (ancho_nave + self.alto) - 16  # Descontamos 4 esquinas

    def calcular_costo_aluminio(self):
        precios_acabado = {
            "Pulido": 50700 / 100, "Lacado Brillante": 54200 / 100,
            "Lacado Mate": 53600 / 100, "Anodizado": 57300 / 100
        }
        perimetro_total = self.calcular_perimetro_nave() * len(self.naves)
        return perimetro_total * precios_acabado[self.acabado]

    def calcular_costo_vidrio(self):
        precios_vidrio = {"Transparente": 8.25, "Bronce": 9.15, "Azul": 12.75}
        area_total = self.calcular_area_nave() * len(self.naves)
        costo_vidrio = area_total * precios_vidrio[self.tipo_vidrio]
        if self.esmerilado:
            costo_vidrio += area_total * 5.20
        return costo_vidrio

    def calcular_costo_esquinas(self):
        return 4310 * 4

    def calcular_costo_chapa(self):
        return 16200 if "X" in self.estilo else 0

    def calcular_costo_total(self):
        return (self.calcular_costo_aluminio() +
                self.calcular_costo_vidrio() +
                self.calcular_costo_esquinas() +
                self.calcular_costo_chapa())

    def validar_dimensiones(self):
        ancho_nave, _ = self.calcular_ancho_naves()
        if ancho_nave <= 1.5 or self.alto <= 1.5:
            raise ValueError("Las dimensiones de la nave son demasiado pequeñas.")
