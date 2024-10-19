import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.ventana import Ventana
from app.cotizacion import Cotizacion
from app.cliente import Cliente
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text

class Cliente:
    def __init__(self, nombre, tipo_cliente, direccion, empresa):
        self.nombre = nombre
        self.tipo_cliente = tipo_cliente
        self.direccion = direccion
        self.empresa = empresa

class Cotizacion:
    def __init__(self, cliente, ventanas, descuento=0):
        self.cliente = cliente
        self.ventanas = ventanas
        self.descuento = descuento

    def calcular_total(self):
        total = sum(ventana.calcular_costo_total() for ventana in self.ventanas)
        if self.descuento > 0:
            total *= (1 - self.descuento / 100)
        return total

    def generar_reporte(self):
        # Generar un reporte sencillo de la cotización
        reporte = f"Cotización para {self.cliente.nombre}\n"
        reporte += f"Cliente: {self.cliente.nombre} - {self.cliente.tipo_cliente}\n"
        reporte += f"Dirección: {self.cliente.direccion}\n"
        reporte += f"Empresa: {self.cliente.empresa}\n"
        reporte += "Ventanas:\n"
        for ventana in self.ventanas:
            reporte += f"- {ventana.estilo} ({ventana.ancho}x{ventana.alto}) - Costo: {ventana.calcular_costo_total()}\n"
        reporte += f"Descuento: {self.descuento}%\n"
        reporte += f"Total a pagar: {self.calcular_total()}\n"
        return reporte

class SistemaCotizacion:
    def __init__(self):
        self.clientes = []
        self.ventanas = []
        self.cotizaciones = []

    def menu_principal(self):
        while True:
            print("\n[1] Registrar ventana")
            print("[2] Registrar cliente")
            print("[3] Registrar cotización")
            print("[4] Ver cotizaciones")
            print("[5] Ver clientes")
            print("[6] Ver ventanas registradas")
            print("[7] Salir")

            opcion = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "6", "7"])

            if opcion == "1":
                self.registrar_ventana()
            elif opcion == "2":
                self.registrar_cliente()
            elif opcion == "3":
                self.registrar_cotizacion()
            elif opcion == "4":
                self.ver_cotizaciones()
            elif opcion == "5":
                self.ver_clientes()
            elif opcion == "6":
                self.ver_ventanas()
            elif opcion == "7":
                print("Saliendo...")
                break

    def registrar_ventana(self):
        estilo = Prompt.ask("Ingrese el estilo de la ventana (O, XO, OXXO, OXO)")
        ancho = float(Prompt.ask("Ingrese el ancho de la ventana en cm"))
        alto = float(Prompt.ask("Ingrese el alto de la ventana en cm"))
        acabado = Prompt.ask("Ingrese el tipo de acabado (Pulido, Lacado Brillante, Lacado Mate, Anodizado)")
        tipo_vidrio = Prompt.ask("Ingrese el tipo de vidrio (Transparente, Bronce, Azul)")
        esmerilado = Prompt.ask("¿Es vidrio esmerilado? (s/n)", choices=["s", "n"]) == "s"

        ventana = Ventana(estilo, ancho, alto, acabado, tipo_vidrio, esmerilado)
        self.ventanas.append(ventana)
        print("Ventana registrada exitosamente.")

    def registrar_cliente(self):
        nombre = Prompt.ask("Ingrese el nombre del cliente")
        tipo_cliente = Prompt.ask("Ingrese el tipo de cliente")
        direccion = Prompt.ask("Ingrese la dirección del cliente")
        empresa = Prompt.ask("Ingrese la empresa")

        cliente = Cliente(nombre, tipo_cliente, direccion, empresa)
        self.clientes.append(cliente)
        print("Cliente registrado exitosamente.")

    def registrar_cotizacion(self):
    # Si no hay clientes o ventanas registrados, no podemos proceder
        if not self.clientes:
            print("No hay clientes registrados. Registre un cliente primero.")
            return
        if not self.ventanas:
            print("No hay ventanas registradas. Registre al menos una ventana primero.")
            return

    # Seleccionar cliente
        cliente_index = self.seleccionar_cliente()
        cliente_seleccionado = self.clientes[cliente_index]

        # Seleccionar ventanas
        ventanas_seleccionadas = self.seleccionar_ventanas()

        # Aplicar descuento si corresponde
        descuento = 0
        if len(ventanas_seleccionadas) > 100:
            descuento = 10
            print(f"Se aplicará un descuento del {descuento}% por más de 100 ventanas.")

        # Crear cotización
        cotizacion = Cotizacion(cliente_seleccionado, ventanas_seleccionadas, descuento)
        self.cotizaciones.append(cotizacion)

        # Calcular el total de la cotización y mostrar el resultado
        total = cotizacion.calcular_total()
        print(f"El costo total de la cotización es: ${total:.2f}")


    def seleccionar_cliente(self):
        # Mostrar lista de clientes registrados
        console = Console()
        table = Table(title="Clientes Registrados")
        table.add_column("ID", justify="center")
        table.add_column("Nombre")
        table.add_column("Tipo de Cliente")
        table.add_column("Dirección")
        table.add_column("Empresa")

        for idx, cliente in enumerate(self.clientes):
            table.add_row(str(idx), cliente.nombre, cliente.tipo_cliente, cliente.direccion)

        console.print(table)

        cliente_index = int(Prompt.ask("Seleccione el ID del cliente"))
        return cliente_index

    def seleccionar_ventanas(self):
        # Mostrar lista de ventanas registradas
        console = Console()
        table = Table(title="Ventanas Registradas")
        table.add_column("ID", justify="center")
        table.add_column("Estilo")
        table.add_column("Dimensiones (Ancho x Alto)")
        table.add_column("Tipo de Vidrio")
        table.add_column("Esmerilado")

        for idx, ventana in enumerate(self.ventanas):
            esmerilado_str = "s" if ventana.esmerilado else "No"
            table.add_row(str(idx), ventana.estilo, f"{ventana.ancho}x{ventana.alto}", ventana.tipo_vidrio, esmerilado_str)

        console.print(table)

        indices_ventanas = Prompt.ask("Seleccione los ID de las ventanas separados por comas (ej: 1,2,3)") #si el cliente necesita varios tipos de ventana este sistema le deja seleccionar cuales ventanas desea
        indices_ventanas = [int(idx) for idx in indices_ventanas.split(",")]

        return [self.ventanas[idx] for idx in indices_ventanas]

    def ver_cotizaciones(self):
        # Mostrar las cotizaciones realizadas
        if not self.cotizaciones:
            print("No hay cotizaciones registradas.")
            return

        for idx, cotizacion in enumerate(self.cotizaciones):
            print(f"Cotización {idx + 1}:")
            print(cotizacion.generar_reporte())

    def ver_clientes(self):
        # Mostrar las cotizaciones realizadas
        if not self.clientes:
            print("No hay clientes registradas.")
            return

        console = Console()
        table = Table(title="Clientes Registrados")
        table.add_column("ID", justify="center")
        table.add_column("Nombre")
        table.add_column("Tipo de Cliente")
        table.add_column("Dirección")
        table.add_column("Empresa")

        for idx, cliente in enumerate(self.clientes):
            table.add_row(str(idx), cliente.nombre, cliente.tipo_cliente, cliente.direccion, cliente.empresa)

        console.print(table)

    def ver_ventanas(self):
        # Mostrar las cotizaciones realizadas
        if not self.ventanas:
            print("No hay ventanas registradas.")
            return
        
        console = Console()
        table = Table(title="Ventanas Registradas")
        table.add_column("ID", justify="center")
        table.add_column("Estilo")
        table.add_column("Dimensiones (Ancho x Alto)")
        table.add_column("Tipo de Vidrio")
        table.add_column("Esmerilado")

        for idx, ventana in enumerate(self.ventanas):
            esmerilado_str = "s" if ventana.esmerilado else "No"
            table.add_row(str(idx), ventana.estilo, f"{ventana.ancho}x{ventana.alto}", ventana.tipo_vidrio, esmerilado_str)

        console.print(table)
                    
# Ejecución principal
if __name__ == "__main__":
    sistema = SistemaCotizacion()
    sistema.menu_principal()