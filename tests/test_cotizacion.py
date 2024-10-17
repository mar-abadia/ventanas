import pytest # type: ignore
from app.cotizacion import Cotizacion 
from app.cliente import Cliente  
from app.ventana import Ventana  

class TestCotizacion:

    @pytest.fixture
    def cotizacion(self):
        # Configuramos una lista de ventanas y un cliente
        ventanas = [Ventana(estilo="XO", ancho=120, alto=150, acabado="Pulido", tipo_vidrio="Transparente") for _ in range(101)]
        cliente = Cliente(nombre="Constructora ABC", empresa="ABC Construcciones", cantidad_ventanas=101)
        return Cotizacion(cliente=cliente, ventanas=ventanas)

    def test_descuento_aplicado(self, cotizacion):
        # Verificamos que se aplique el descuento del 10% si hay más de 100 ventanas
        total = cotizacion.calcular_total()
        total_sin_descuento = sum(ventana.calcular_costo_total() for ventana in cotizacion.ventanas)
        assert total == pytest.approx(total_sin_descuento * 0.9)

    def test_sin_descuento(self, cotizacion):
        # Verificamos que no se aplique el descuento si hay menos de 100 ventanas
        cotizacion.cliente.cantidad_ventanas = 99
        total = cotizacion.calcular_total()
        total_sin_descuento = sum(ventana.calcular_costo_total() for ventana in cotizacion.ventanas)
        assert total == pytest.approx(total_sin_descuento)
