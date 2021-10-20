from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import hashlib
import os

app = Flask(import_name=__name__)
# Flask por default trabaja con sesiones
# basadas en cookies. Las sesiones se encriptan
# mediante una llave secreta: https://youtu.be/EqtHn_xsxTQ
app.secret_key = os.urandom(24)

# Login


@app.route("/", methods=["GET", "POST"])
def login():
    # Especificar la variable mensaje
    # como caracteres vacios para poder
    # renderizar inicialmente la página
    mensaje = ''
    if request.method == 'POST':
        # Las variables se obtinen a través del
        # attributo name en cada elemento
        id = request.form["id"]
        password = request.form["password"]
        passwordEncode = hashlib.sha256(
            password.encode(encoding="utf-8")).hexdigest()
        with sqlite3.connect("hospital.db") as connection:
            # Ver información sobre el tema en
            # https://rico-schmidt.name/pymotw-3/sqlite3/index.html > Objetos de fila
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM usuario WHERE id = ? AND password = ?",
                [id, passwordEncode])
            # Obtenemos la primera fila y guardarla como una variable
            # llamada row
            row = cursor.fetchone()
            # Aquí verificamos que la fila no este vacía
            # Si no esta vacía procedemos
            if row:
                # Para ver el tema de sesiones consultar:
                # https://youtu.be/2Zz97NVbH0U y https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/
                # Creamos una sesión
                # Esta variable ya la teniamos definida
                session["id"] = id
                # Extraemos la variable rol de la fila para definir
                # a que parte redirigir al usuario
                session["rol"] = row["rol"]
                # Debemos verificar si el usuario esta activo
                session["estado"] = row["estado"]
                # Vamos a utilizar esta parte para obtener los nombres
                # del usuario
                session["nombres"] = row["nombres"]
                if session["rol"] == 'superadministrador' and session["estado"] == 'activo':
                    # Ver https://gist.github.com/rduplain/2173954
                    # respecto a utilizar redirect
                    return redirect(url_for('superAdministrador'))
                elif session["rol"] == 'medico' and session["estado"] == 'activo':
                    return redirect(url_for('medico'))
                elif session["rol"] == 'paciente' and session["estado"] == 'activo':
                    return redirect(url_for('paciente'))
                elif session["estado"] == 'inactivo':
                    mensaje = "El usuario se encuentra inactivo por favor comunicarse con el administrador del sistema"
            # En caso que este vacía redireccionamos nuevamente al
            # usuario a la página de login
            else:
                mensaje = "El documento de identidad o la contraseña son incorrectos o no existen"
    return render_template("login.html", mensaje=mensaje)


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


@app.route("/recuperarContrasena", methods=["GET", "POST"])
def recuperarContrasena():
    return render_template("recuperarContrasena.html")


@app.route("/generarNuevaContrasena")
def generarNuevaContrasena():
    return render_template("generarNuevaContrasena.html")

# Rutas medico


@app.route("/medico", methods=["GET", "POST"])
def medico():
    if request.method == 'get':
        docPaciente = request.form["docPaciente"]
        docMedico = request.form["docMedico"]
        nombreMedico = request.form["nombreMedico"]
        cargo = request.form["cargo"]
        idCita = request.form["idCita"]
        fechaAgenda = request.form["fechaAgenda"]
        # Consultar y mostrar
        with sqlite3.connect("hospital.db") as connection:
            # Lugar donde almacenamos todo lo que vamos a ejecutar
            cursor = connection.cursor()
            cursor.execute("INSERT INTO usuario VALUES (?, ?, ?, ?, ?)",
                           [id, nombres, rol, password, estado])
            cursor.execute("INSERT INTO paciente VALUES (?, ?, ?, ?, ?, ?)",
                           [id, edad, profesion, email, genero, tipoSangre])
            connection.commit()
    return render_template("medico.html")


@app.route("/medico/historiaClinica", methods=["GET", "POST"])
def historia_clinica():
    if request.method == 'get':
        docPaciente = request.form["docPaciente"]
        nombrePaciente = request.form["nombrePaciente"]
        genero = request.form["genero"]
        edad = request.form["edad"]
        correo = request.form["correo"]
        tipoRh = request.form["tipoRh"]
        numeroContacto = request.form["numeroContacto"]
        direccion = request.form["direccion"]
        fechaInicio = request.form["fechaInicio"]
        fechaFinal = request.form["fechaFinal"]
        historiaClinica = request.form["historiaClinica"]
        # Consultar y mostrar
        with sqlite3.connect("hospital.db") as connection:
            # Lugar donde almacenamos todo lo que vamos a ejecutar
            cursor = connection.cursor()
            cursor.execute("INSERT INTO usuario VALUES (?, ?, ?, ?, ?)",
                           [id, nombres, rol, password, estado])
            cursor.execute("INSERT INTO paciente VALUES (?, ?, ?, ?, ?, ?)",
                           [id, edad, profesion, email, genero, tipoSangre])
            connection.commit()
    return render_template("historiaClinica.html")


@app.route("/medico/consultaMedica", methods=["get", "post"])
def consulta_medica():
    if request.method == 'get':
        docPaciente = request.form["docPaciente"]
        nombrePaciente = request.form["nombrePaciente"]
        genero = request.form["genero"]
        edad = request.form["edad"]
        tipoRh = request.form["tipoRh"]
        # Consultar y mostrar
        with sqlite3.connect("hospital.db") as connection:
            # Lugar donde almacenamos todo lo que vamos a ejecutar
            cursor = connection.cursor()
            cursor.execute("INSERT INTO usuario VALUES (?, ?, ?, ?, ?)",
                           [id, nombres, rol, password, estado])
            cursor.execute("INSERT INTO paciente VALUES (?, ?, ?, ?, ?, ?)",
                           [id, edad, profesion, email, genero, tipoSangre])
            connection.commit()
    if request.method == 'post':
        sintomas = request.form["sintomas"]
        antecedentes = request.form["nombreMedico"]
        cirugias = request.form["cirugias"]
        diagnostico = request.form["diagnostico"]
        peso = request.form["peso"]
        altura = request.form["altura"]
        precionArterial = request.form["precion"]
        temperatura = request.form["temperatura"]
        farmacologia = request.form["farmacologia"]
        parejas = request.form["parejas"]
        embarazos = request.form["embarazos"]
        nacidosVivos = request.form["nacidosVivos"]
        partoNatural = request.form["partoNatural"]
        metodoAnticonceptivo = request.form["metodoAnticonceptivo"]
        drogas = request.form["dogras"]
        examenesMedicos = request.form["autorizacionExamenes"]
        ordenMedicamentos = request.form["ordenesMedicamentos"]
        # Consultar y mostrar
        with sqlite3.connect("hospital.db") as connection:
            # Lugar donde almacenamos todo lo que vamos a ejecutar
            cursor = connection.cursor()
            cursor.execute("INSERT INTO historiaClinica VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           [id, sintomas, antecedentes, cirugias, diagnostico, examenesMedicos, peso, altura, precionArterial, temperatura, farmacologia, parejas, embarazos, nacidosVivos, partoNatural, metodoAnticonceptivo, drogas, ordenMedicamentos])
            connection.commit()
    return render_template("consultaMedica.html")

# Rutas Super Administrador


@app.route("/superAdministrador")
def superAdministrador():
    return render_template("superAdministrador.html")


@app.route("/superAdministrador/dashboard", methods=["GET", "POST"])
def superAdministradorDashboard():
    return render_template("dashboard.html")


@app.route("/superAdministrador/historiaClinica", methods=["GET", "POST"])
def superAdministradorHistoriaClinica():
    return render_template("historiaClinicaSuper.html")


@app.route("/superAdministrador/aperturaAgenda", methods=["GET", "POST"])
def superAdministradorAperturaAgenda():
    return render_template("aperturaAgenda.html")

# Rutas Paciente


@app.route("/paciente")
def paciente():
    # En esta parte recuerde que la sesión es como un diccionario
    # Es decir si la llave se encuentra en el diccionario entonces
    # se obtiene true
    if 'id' in session:
        nombres = session["nombres"]
    return render_template("paciente.html", nombres=nombres)


@app.route("/paciente/citaMedica", methods=["GET", "POST"])
def citaMedica():
    if ('id' in session) and (request.method == 'POST'):
        fechaInicialAgendaCita = request.form["fechaInicialAgendaCita"]
        fechaFinalAgendaCita = request.form["fechaFinalAgendaCita"]
        estado = 'disponible'
        with sqlite3.connect("hospital.db") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM agendaMedica WHERE estado = ? AND (fecha BETWEEN ? AND ?)",
                           [estado, fechaInicialAgendaCita, fechaFinalAgendaCita])
            # Consultar esta página para mostrar datos en una tabla
            # https://pythonbasics.org/flask-sqlite/
    return render_template("citaMedica.html")


@ app.route("/paciente/examenMedico", methods=["GET", "POST"])
def examenMedico():
    return render_template("examenMedico.html")


@ app.route("/paciente/historiaClinica", methods=["GET", "POST"])
def pacienteHistoriaClinica():
    return render_template("pacienteHistoriaClinica.html")


if __name__ == '__main__':
    app.run(debug=True)
