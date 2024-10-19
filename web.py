from flask import Flask, render_template, request, redirect, url_for, flash
from app.ventana import Ventana
from app.cotizacion import Cotizacion
from app.cliente import Cliente
from flask import render_template


app = Flask(__name__)
app.secret_key = "clave_secreta"

# Datos en memoria simulando una base de datos
clientes = []
ventanas = []
cotizaciones = []

@app.route('/')
def menu_principal():
    return render_template('menu_principal.html')

# Registrar ventana
@app.route('/registrar_ventana', methods=['GET', 'POST'])
def registrar_ventana():
    if request.method == 'POST':
        estilo = request.form['estilo']
        ancho = float(request.form['ancho'])
        alto = float(request.form['alto'])
        acabado = request.form['acabado']
        tipo_vidrio = request.form['tipo_vidrio']
        esmerilado = request.form['esmerilado'] == 's'

        ventana = Ventana(estilo, ancho, alto, acabado, tipo_vidrio, esmerilado)
        ventanas.append(ventana)
        flash('Ventana registrada exitosamente.')
        return redirect(url_for('menu_principal'))
    
    return render_template('registrar_ventana.html')

# Registrar cliente
@app.route('/registrar_cliente', methods=['GET', 'POST'])
def registrar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo_cliente = request.form['tipo_cliente']
        direccion = request.form['direccion']
        empresa = request.form['empresa']

        cliente = Cliente(nombre, tipo_cliente, direccion, empresa)
        clientes.append(cliente)
        flash('Cliente registrado exitosamente.')
        return redirect(url_for('menu_principal'))
    
    return render_template('registrar_cliente.html')

# Registrar cotización
@app.route('/registrar_cotizacion', methods=['GET', 'POST'])
def registrar_cotizacion():
    if not clientes or not ventanas:
        flash("Debe registrar al menos un cliente y una ventana antes de crear una cotización.")
        return redirect(url_for('menu_principal'))

    if request.method == 'POST':
        cliente_id = int(request.form['cliente'])
        ventanas_ids = request.form.getlist('ventanas')
        ventanas_seleccionadas = [ventanas[int(id)] for id in ventanas_ids]

        cliente = clientes[cliente_id]
        cotizacion = Cotizacion(cliente, ventanas_seleccionadas)
        cotizaciones.append(cotizacion)

        flash(f'Cotización creada con éxito. Total: $' + {cotizacion.calcular_total()})
        return redirect(url_for('ver_cotizaciones'))

    return render_template('registrar_cotizacion.html', clientes=clientes, ventanas=ventanas)

# Ver cotizaciones
@app.route('/ver_cotizaciones')
def ver_cotizaciones():
    return render_template('ver_cotizaciones.html', cotizaciones=cotizaciones)

# Ver clientes
@app.route('/ver_clientes')
def ver_clientes():
    return render_template('ver_clientes.html', clientes=clientes)

# Ver ventanas
@app.route('/ver_ventanas')
def ver_ventanas():
    return render_template('ver_ventanas.html', ventanas=ventanas)

if __name__ == '__main__':
    app.run(debug=True)
