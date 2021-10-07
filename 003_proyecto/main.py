from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("login.html")

# Rutas medico
@app.route("/medico")
def medico():
    return render_template("medico.html")

@app.route("/medico/historiaClinica")
def historia_clinica():
    return render_template("historiaClinica.html")

@app.route("/medico/consultaMedica")
def consulta_medica():
    return render_template("consultaMedica.html")

# Rutas Super Administrador   
@app.route("/superAdministrador")
def superAdministrador():
    return render_template("superAdministrador.html")

@app.route("/superAdministrador/agendaMedica")
def superAdministradorAgendaMedica():
    return render_template("agendaSuper.html")

@app.route("/superAdministrador/dashboard")
def superAdministradorDashboard():
    return render_template("dashboard.html")

@app.route("/superAdministrador/historiaClinica")
def superAdministradorHistoriaClinica():
    return render_template("historiaClinicaSuper.html")

@app.route("/superAdministrador/aperturaAgenda")
def superAdministradorAperturaAgenda():
    return render_template("aperturaAgenda.html")

#Rutas Paciente
@app.route("/paciente")
def paciente():
    return render_template("paciente.html")

app.run(debug=True)

