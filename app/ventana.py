from app.nave import Nave

class Ventana:
    def __init__(self, estilo, ancho, alto, acabado, tipo_vidrio, esmerilado=False):
        self.estilo = estilo
        self.ancho = ancho
        self.alto = alto
        self.acabado = acabado
        self.tipo_vidrio = tipo_vidrio
        self.esmerilado = esmerilado
        self.naves = self.crear_naves(ancho, alto, acabado, tipo_vidrio, esmerilado)

    def calcular_ancho_naves(self):
        estilo_naves = {
            "O": 1,
            "XO": 2,
            "OXO": 3,
            "OXXO": 4,
        }
        naves = estilo_naves[self.estilo]
        return self.ancho / naves, naves

    def calcular_area_nave(self):
        ancho_nave, _ = self.calcular_ancho_naves()
        return (ancho_nave - 1.5) * (self.alto - 1.5)

    def calcular_perimetro_nave(self):
        ancho_nave, _ = self.calcular_ancho_naves()
        return 2 * (ancho_nave + self.alto) - 4 * 4

    def calcular_costo_aluminio(self):
        costo_por_cm_lineal = {
            "Pulido": 50700 / 100,
            "Lacado Brillante": 54200 / 100,
            "Lacado Mate": 53600 / 100,
            "Anodizado": 57300 / 100
        }
        perimetro_total = self.calcular_perimetro_nave() * self.calcular_ancho_naves()[1]
        return perimetro_total * costo_por_cm_lineal[self.acabado]

    def calcular_costo_vidrio(self):
        costo_por_cm2 = {
            "Transparente": 8.25,
            "Bronce": 9.15,
            "Azul": 12.75
        }
        area_total = self.calcular_area_nave() * self.calcular_ancho_naves()[1]
        costo_vidrio = area_total * costo_por_cm2[self.tipo_vidrio]
        if self.esmerilado:
            costo_vidrio += area_total * 5.20
        return costo_vidrio

    def calcular_costo_esquinas(self):
        return 4310 * 4

    def calcular_costo_chapa(self):
        if "X" in self.estilo:
            return 16200
        return 0

    def calcular_costo_total(self):
        return self.calcular_costo_aluminio() + self.calcular_costo_vidrio() + self.calcular_costo_esquinas() + self.calcular_costo_chapa()

    def crear_naves(self, ancho, alto, acabado, tipo_vidrio, esmerilado):
        naves = []
        ancho_nave, num_naves = self.calcular_ancho_naves()
        for _ in range(num_naves):
            nave = Nave(tipo_vidrio, ancho_nave, alto, acabado, esmerilado)
            naves.append(nave)
        return naves

    def validar_dimensiones_naves(self):
        ancho_nave, _ = self.calcular_ancho_naves()
        if ancho_nave <= 1.5 or self.alto <= 1.5:
            raise ValueError("Las dimensiones de la nave son demasiado pequeñas.")

    def validar_tamaño_vidrio(self):
        ancho_nave, _ = self.calcular_ancho_naves()
        if self.ancho - 1.5 < ancho_nave:
            raise ValueError("El vidrio debe ser 1.5 cm más pequeño que la nave.")
