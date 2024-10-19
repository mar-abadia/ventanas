import pytest 
from app.cliente import Cliente

class TestCliente:
    
    @pytest.fixture
    def cliente(self):
        # Creamos una instancia de Cliente para usar en las pruebas
        return Cliente(nombre="Juan Pérez", empresa="Construcciones ABC", cantidad_ventanas=50)

    def test_atributos_cliente(self, cliente):
        # Verificamos que los atributos del cliente sean correctos
        assert cliente.nombre == "Juan Pérez"
        assert cliente.empresa == "Construcciones ABC"
        assert cliente.cantidad_ventanas == 50

    def test_actualizar_cantidad_ventanas(self, cliente):
        # Verificamos que se puede actualizar la cantidad de ventanas solicitadas
        cliente.cantidad_ventanas = 120
        assert cliente.cantidad_ventanas == 120