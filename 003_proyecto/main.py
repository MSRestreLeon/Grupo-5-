from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/paciente")
def paciente():
    return render_template("paciente.html")


@app.route("/medico")
def medico():
    return render_template("medico.html")


@app.route("/superAdministrador")
def superAdministrador():
    return render_template("superAdministrador.html")
