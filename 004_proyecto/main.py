# Importar módulos o librerias
# Importar la clase Flask, el método render_template
from flask import Flask, render_template, request
import sqlite3
# Importo la librería para cubrir el password
import hashlib

# Generar una instacia de la clase Flask
# para que pueda encontrar los archivos templates
# y statics con al argument __name__
# Ver más detalles en https://flask.palletsprojects.com/en/2.0.x/api/
app = Flask(import_name=__name__)

# Login


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form["id"]
        password = request.form["password"]
        passwordEncode = hashlib.sha256(
            password.encode(encoding="utf-8")).hexdigest()
        with sqlite3.connect("hospital.db") as connection:
            connection.row_factory = sqlite3.Row
            # Lugar donde almacenamos todo lo que vamos a ejecutar
            cursor = connection.cursor()
            cursor.execute("INSERT INTO prueba VALUES (?)", [id])
            # Finalizar la instrucción de ejecución
            connection.commit()
    return render_template("login.html")


@app.route("/registroPaciente", methods=['GET', 'POST'])
def registroPaciente():
    if request.method == 'POST':
        nombres = request.form["nombres"]
        id = request.form["id"]
        edad = request.form["edad"]
        profesion = request.form["profesion"]
        email = request.form["email"]
        genero = request.form["genero"]
        tipoSangre = request.form["tipoSangre"]
        password = request.form["password"]
        # Ver https://www.geeksforgeeks.org/md5-hash-python/
        # Codificar el password de tal manera que pueda ser
        # aceptado por una función hash: password.encode(encoding="utf-8")
        # Aplicar la función hash correspondiente hashlib.sha256()
        # Generar la contraseña codificada en un formato hexadecimal: .hexdigest
        passwordEncode = hashlib.sha256(
            password.encode(encoding="utf-8")).hexdigest()
        rol = 'paciente'
        estado = 'activo'
        with sqlite3.connect("hospital.db") as connection:
            # Lugar donde almacenamos todo lo que vamos a ejecutar
            cursor = connection.cursor()
            cursor.execute("INSERT INTO usuario VALUES (?, ?, ?, ?, ?)",
                           [id, nombres, rol, passwordEncode, estado])
            cursor.execute("INSERT INTO paciente VALUES (?, ?, ?, ?, ?, ?)",
                           [id, edad, profesion, email, genero, tipoSangre])
            connection.commit()
    return render_template("registroPaciente.html")


# Ver detalles en https://es.stackoverflow.com/questions/32165/qu%C3%A9-es-if-name-main/32185
if __name__ == '__main__':
    app.run(debug=True)
