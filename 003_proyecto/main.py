from flask import Flask, render_template, request
import sqlite3

app = Flask(import_name=__name__)

# Login


@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    return render_template("registrarse.html")


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
        #Consultar y mostrar
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
        #Consultar y mostrar
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
        #Consultar y mostrar
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
        #Consultar y mostrar
        with sqlite3.connect("hospital.db") as connection:
            # Lugar donde almacenamos todo lo que vamos a ejecutar
            cursor = connection.cursor()
            cursor.execute("INSERT INTO historiaClinica VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           [id, sintomas, antecedentes, cirugias, diagnostico, examenesMedicos, peso, altura, precionArterial, temperatura, farmacologia, parejas, embarazos, nacidosVivos, partoNatural, metodoAnticonceptivo, drogas, ordenMedicamentos ])
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
    return render_template("paciente.html")


@app.route("/paciente/citaMedica", methods=["GET", "POST"])
def citaMedica():
    return render_template("citaMedica.html")


@app.route("/paciente/examenMedico", methods=["GET", "POST"])
def examenMedico():
    return render_template("examenMedico.html")


@app.route("/paciente/historiaClinica", methods=["GET", "POST"])
def pacienteHistoriaClinica():
    return render_template("pacienteHistoriaClinica.html")


if __name__ == '__main__':
    app.run(debug=True)
