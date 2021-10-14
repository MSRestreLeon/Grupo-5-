from flask import Flask, render_template

app = Flask(__name__)

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
    return render_template("medico.html")


@app.route("/medico/historiaClinica", methods=["GET", "POST"])
def historia_clinica():
    return render_template("historiaClinica.html")


@app.route("/medico/consultaMedica", methods=["GET", "POST"])
def consulta_medica():
    return render_template("consultaMedica.html")

# Rutas Super Administrador


@app.route("/superAdministrador")
def superAdministrador():
    return render_template("superAdministrador.html")


@app.route("/superAdministrador/agendaMedica", methods=["GET", "POST"])
def superAdministradorAgendaMedica():
    return render_template("agendaSuper.html")


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


app.run(debug=True)
