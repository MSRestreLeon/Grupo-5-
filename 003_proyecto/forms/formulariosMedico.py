from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class medico(FlaskForm):
    cerarSesion = SubmitField("Cerar")
    documentoIdentidad = StringField("")
    nombre = StringField("")
    cargo = StringField("")
    edad = StringField("")
    correo = StringField("")
    editar = SubmitField("")
    fecha = StringField("")
    consultar = SubmitField("")
    documentoHis = StringField("Usuario", validators=[
        DataRequired(message="Documento de identidad es obligartorio")])
    consultarHis = SubmitField("")
class medicoHis(FlaskForm):
    cerarSesion = SubmitField("")
    home = SubmitField("")
    back = SubmitField("")
    documentoIdentidad = StringField("")
    nombre = StringField("")
    genero = StringField("")
    edad = StringField("")
    
    correo = StringField("")
    tipoRh = StringField("")
    numeroContacto = StringField("")
    direccionRecidencia = StringField("")
    fechaInicial = StringField("")
    fechaFinal = StringField("")
    ver = StringField("")
    imprimir = StringField("")
    generarPdf = StringField("")