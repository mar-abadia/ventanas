from app.main import Ventana, Cotizacion  
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

class Ventana:
    def __init__(self, estilo, ancho, alto, acabado, tipo_vidrio, esmerilado):
        self.estilo = estilo
        self.ancho = ancho
        self.alto = alto
        self.acabado = acabado
        self.tipo_vidrio = tipo_vidrio
        self.esmerilado = esmerilado

    def calcular_costo(self):
        costo_base = 1000  # Ejemplo simplificado
        if self.esmerilado:
            costo_base += 200
        return costo_base

class Cotizacion:
    def __init__(self, cliente, ventanas):
        self.cliente = cliente
        self.ventanas = ventanas

    def calcular_total(self):
        return sum(ventana.calcular_costo() for ventana in self.ventanas)

class CotizacionForm(FlaskForm):
    cliente = StringField('Nombre del Cliente', validators=[DataRequired()])
    estilo = SelectField('Estilo de Ventana', choices=[('O', 'O'), ('XO', 'XO'), ('OXXO', 'OXXO'), ('OXO', 'OXO')], validators=[DataRequired()])
    ancho = FloatField('Ancho (cm)', validators=[DataRequired(), NumberRange(min=10)])
    alto = FloatField('Alto (cm)', validators=[DataRequired(), NumberRange(min=10)])
    acabado = SelectField('Acabado de Aluminio', choices=[('Pulido', 'Pulido'), ('Lacado Brillante', 'Lacado Brillante'), ('Lacado Mate', 'Lacado Mate'), ('Anodizado', 'Anodizado')], validators=[DataRequired()])
    tipo_vidrio = SelectField('Tipo de Vidrio', choices=[('Transparente', 'Transparente'), ('Bronce', 'Bronce'), ('Azul', 'Azul')], validators=[DataRequired()])
    esmerilado = BooleanField('Vidrio Esmerilado')
    submit = SubmitField('Calcular Cotización')

@app.route("/", methods=["GET", "POST"])
def cotizar():
    form = CotizacionForm()
    if form.validate_on_submit():
        ventana = Ventana(
            estilo=form.estilo.data,
            ancho=form.ancho.data,
            alto=form.alto.data,
            acabado=form.acabado.data,
            tipo_vidrio=form.tipo_vidrio.data,
            esmerilado=form.esmerilado.data
        )
        cotizacion = Cotizacion(cliente=form.cliente.data, ventanas=[ventana])
        total = cotizacion.calcular_total()

        flash(f'Cotización creada para {form.cliente.data} por un total de ${total:.2f}')
        return redirect(url_for('resultado', total=total, cliente=form.cliente.data))
    return render_template("cotizacion.html", form=form)

@app.route("/resultado")
def resultado():
    total = request.args.get('total')
    cliente = request.args.get('cliente')
    return render_template("resultado.html", total=total, cliente=cliente)

@app.route("/descargar_cotizacion")
def descargar_cotizacion():
    cliente = request.args.get('cliente')
    total = request.args.get('total')

    # Crear el PDF en memoria
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.drawString(100, 750, f"Cotización para: {cliente}")
    pdf.drawString(100, 730, f"Total: ${total} USD")
    pdf.drawString(100, 710, "Gracias por su preferencia.")
    pdf.showPage()
    pdf.save()

    pdf_buffer.seek(0)  # Volver al inicio del buffer

    # Descargar el archivo PDF
    return send_file(pdf_buffer, as_attachment=True, download_name=f"Cotizacion_{cliente}.pdf", mimetype='application/pdf')

if __name__ == "__main__":
    app.run(debug=True)
