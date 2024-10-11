from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from app.main import Ventana, Cotizacion  
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('cotizacion.html')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# Simulación de las clases de Ventana, Cliente y Cotización
class Ventana:
    def __init__(self, estilo, ancho, alto, acabado, tipo_vidrio, esmerilado):
        self.estilo = estilo
        self.ancho = ancho
        self.alto = alto
        self.acabado = acabado
        self.tipo_vidrio = tipo_vidrio
        self.esmerilado = esmerilado

    def calcular_costo(self):
        # Simplificación del cálculo de costos
        costo_base = 1000
        if self.esmerilado:
            costo_base += 200
        return costo_base

class Cotizacion:
    def __init__(self, cliente, ventanas):
        self.cliente = cliente
        self.ventanas = ventanas

    def calcular_total(self):
        return sum([ventana.calcular_costo() for ventana in self.ventanas])

# Formulario de Cotización
class CotizacionForm(FlaskForm):
    cliente = StringField('Nombre del Cliente', validators=[DataRequired()])
    estilo = SelectField('Estilo de Ventana', choices=[('O', 'O'), ('XO', 'XO'), ('OXXO', 'OXXO'), ('OXO', 'OXO')], validators=[DataRequired()])
    ancho = FloatField('Ancho (cm)', validators=[DataRequired(), NumberRange(min=10, message="El ancho debe ser mayor a 10 cm")])
    alto = FloatField('Alto (cm)', validators=[DataRequired(), NumberRange(min=10, message="El alto debe ser mayor a 10 cm")])
    acabado = SelectField('Acabado de Aluminio', choices=[('Pulido', 'Pulido'), ('Lacado Brillante', 'Lacado Brillante'), ('Lacado Mate', 'Lacado Mate'), ('Anodizado', 'Anodizado')], validators=[DataRequired()])
    tipo_vidrio = SelectField('Tipo de Vidrio', choices=[('Transparente', 'Transparente'), ('Bronce', 'Bronce'), ('Azul', 'Azul')], validators=[DataRequired()])
    esmerilado = BooleanField('Vidrio Esmerilado')
    submit = SubmitField('Calcular Cotización')

# Ruta principal para mostrar el formulario
@app.route("/", methods=["GET", "POST"])
def cotizar():
    form = CotizacionForm()
    if form.validate_on_submit():
        # Crear una instancia de Ventana a partir del formulario
        ventana = Ventana(
            estilo=form.estilo.data,
            ancho=form.ancho.data,
            alto=form.alto.data,
            acabado=form.acabado.data,
            tipo_vidrio=form.tipo_vidrio.data,
            esmerilado=form.esmerilado.data
        )
        # Calcular la cotización
        cotizacion = Cotizacion(cliente=form.cliente.data, ventanas=[ventana])
        total = cotizacion.calcular_total()
        return redirect(url_for('resultado', total=total, cliente=form.cliente.data))
    return render_template("cotizacion.html", form=form)

# Ruta para mostrar el resultado de la cotización
@app.route("/resultado")
def resultado():
    total = request.args.get('total')
    cliente = request.args.get('cliente')
    return render_template("resultado.html", total=total, cliente=cliente)

if __name__ == "__main__":
    app.run(debug=True)
