import pytest # type: ignore
from app.ventana import Ventana  

class TestVentana:

    @pytest.fixture
    def ventana(self):
        # Creamos una instancia de Ventana para usar en las pruebas
        return Ventana(estilo="XO", ancho=120, alto=150, acabado="Pulido", tipo_vidrio="Transparente", esmerilado=False)

    def test_calcular_ancho_naves(self, ventana):
        # Verificamos que el cálculo de ancho por nave sea correcto
        ancho_nave, naves = ventana.calcular_ancho_naves()
        assert naves == 2
        assert ancho_nave == pytest.approx(60)

    def test_calcular_area_nave(self, ventana):
        # Verificamos el cálculo del área de cada nave
        area_nave = ventana.calcular_area_nave()
        assert area_nave == pytest.approx((60 - 1.5) * (150 - 1.5))

    def test_calcular_costo_aluminio(self, ventana):
        # Verificamos el cálculo del costo de aluminio
        costo_aluminio = ventana.calcular_costo_aluminio()
        perimetro_nave = 2 * ((60 - 1.5) + 150) - 16
        naves = 2  # Para el estilo "XO"
        perimetro_total = perimetro_nave * naves
        costo_esperado = perimetro_total * 507

    def test_calcular_costo_vidrio(self, ventana):
        # Verificamos el cálculo del costo del vidrio
        costo_vidrio = ventana.calcular_costo_vidrio()
        area_nave = (60 - 1.5) * (150 - 1.5)
        costo_esperado = area_nave * 2 * 8.25  # precio del vidrio transparente por cm²
        assert costo_vidrio == pytest.approx(costo_esperado)

    def test_calcular_costo_total(self, ventana):
        # Verificamos el cálculo del costo total de la ventana
        costo_total = ventana.calcular_costo_total()
        costo_esperado = ventana.calcular_costo_aluminio() + ventana.calcular_costo_vidrio() + 4310 * 4 + 16200
        assert costo_total == pytest.approx(costo_esperado)
