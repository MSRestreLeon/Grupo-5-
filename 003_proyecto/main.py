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
    agenda=''
    if request.method == 'POST':
        fechaAgenda = request.form["fechaAgenda"]
        docMedico = request.form["docMedico"]
        #Consultar y mostrar
        with sqlite3.connect("hospital.db") as connection:
            # Lugar donde almacenamos todo lo que vamos a ejecutar
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM agendaMedica WHERE idMedico = ? AND fecha = ?",
                [docMedico,fechaAgenda])
            agenda = cursor.fetchall()
            #while matriz != None:
            #    for i in range(len(matriz)):
            #        for n in range(len(matriz[i])):
            #          agenda=matriz[i][n] 
    return render_template("medico.html",agenda=agenda)


@app.route("/medico/historiaClinica", methods=["GET", "POST"])
def historia_clinica():
    historia=''
    if request.method == 'POST':
        docPaciente = request.form["docPaciente"]
        # Consultar y mostrar
        with sqlite3.connect("hospital.db") as connection:
            # Lugar donde almacenamos todo lo que vamos a ejecutar
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM historiaClinica WHERE docPaciente = ? ",
                [docPaciente])
            historia = cursor.fetchall()
        
    return render_template("historiaClinica.html",historia=historia)


@app.route("/medico/consultaMedica", methods=["GET", "POST"])
def consulta_medica():
    mensaje = ''
    if request.method == 'POST':
        id = request.form["idCita"]
        docPaciente = request.form["docPaciente"]
        sintomas = request.form["sintomas"]
        antecedentes = request.form["antecedentes"]
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
            if id == "" or docPaciente == "" or sintomas == "" or antecedentes == "" or cirugias == "" or diagnostico == "" or examenesMedicos == "" or peso == "" or altura == "" or precionArterial == "" or parejas == "" or ordenMedicamentos == "":
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("INSERT INTO historiaClinica (idCitaMedica,docPaciente,sintomas,antecedentes,cirugias,diagnostico,examenesMedicos,peso,altura,presionArterial,temperatura,farmacologia,parejas,embarazos,nacidosVivos,partoNatural,metodoAnticonceptivo,drogas,ordenMedicamentos) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           [id,docPaciente,sintomas,antecedentes,cirugias,diagnostico,examenesMedicos,peso,altura,precionArterial,temperatura,farmacologia,parejas,embarazos,nacidosVivos,partoNatural,metodoAnticonceptivo,drogas,ordenMedicamentos])
                connection.commit()
    return render_template("consultaMedica.html",mensaje=mensaje)

# Rutas Super Administrador


@app.route("/superAdministrador", methods=["GET", "POST"])
def superAdministrador():
    return render_template("superAdministrador.html")

@app.route("/superAdministrador/editarMedico", methods=["GET", "POST"])
def editarMedico():
    if request.method == 'POST':
        docMedico = request.form["docMedico"]
        especialidad = request.form["especialidad"]
        estado = request.form["estado"]
        # Consultar y mostrar
        with sqlite3.connect("hospital.db") as connection:
            # Lugar donde almacenamos todo lo que vamos a ejecutar
            cursor = connection.cursor()
            if (docMedico==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("INSERT INTO medico (id) VALUES (?)",
                        [docMedico])
                cursor.execute("INSERT INTO usuario (id) VALUES (?)",
                        [docMedico])
                connection.commit()
            if (especialidad==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("INSERT INTO medico (especialidad) VALUES (?)",
                        [especialidad])
                connection.commit()
            if (estado==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("INSERT INTO usuario (estado) VALUES (?)",
                        [estado])
                connection.commit()
    return render_template("editarMedico.html")

@app.route("/superAdministrador/dashboard", methods=["GET", "POST"])
def superAdministradorDashboard():
    return render_template("dashboard.html")

@app.route("/superAdministrador/editarPaciente", methods=["GET", "POST"])
def superAdministradorEditarPaciente():
    if request.method == 'POST':
        nombres = request.form["nombres"]
        id = request.form["id"]
        
        edad = request.form["edad"]
        profesion = request.form["profesion"]
        email = request.form["email"]
        genero = request.form["genero"]
        rh = request.form["rh"]
        estado = request.form["estado"]
        # Consultar y mostrar
        with sqlite3.connect("hospital.db") as connection:
            # Lugar donde almacenamos todo lo que vamos a ejecutar
            cursor = connection.cursor()
            if (nombres==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("INSERT INTO medico (id) VALUES (?)",
                        [nombres])
                cursor.execute("INSERT INTO usuario (id) VALUES (?)",
                        [nombres])
                connection.commit()
            if (id==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("INSERT INTO medico (id) VALUES (?)",
                        [id])
                connection.commit()
            
            if (edad==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("INSERT INTO usuario (edad) VALUES (?)",
                        [edad])
                connection.commit()
            
            if (profesion==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("INSERT INTO usuario (profesion) VALUES (?)",
                        [profesion])
                connection.commit()
            if (email==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("INSERT INTO usuario (email) VALUES (?)",
                        [email])
                connection.commit()
            if (genero==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("INSERT INTO usuario (genero) VALUES (?)",
                        [genero])
                connection.commit()

            if (rh==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("INSERT INTO usuario (rh) VALUES (?)",
                        [rh])
                connection.commit()                                
        
            if (estado==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("INSERT INTO usuario (estado) VALUES (?)",
                        [estado])
                connection.commit()
    
    return render_template("editarPaciente.html")


@app.route("/superAdministrador/historiaClinica", methods=["GET", "POST"])
def superAdministradorHistoriaClinica():
    return render_template("historiaClinicaSuper.html")


@app.route("/superAdministrador/aperturaAgenda", methods=["GET", "POST"])
def superAdministradorAperturaAgenda():
    if request.method == 'POST':
        docMedico = request.form["docMedico"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        estado = request.form["estado"]
        
        # Consultar y mostrar
        with sqlite3.connect("hospital.db") as connection:
            # Lugar donde almacenamos todo lo que vamos a ejecutar
            cursor = connection.cursor()
            if (docMedico=="" or fecha=="" or hora=="" or estado==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("INSERT INTO agendaMedica (idMedico,fecha,hora,estado) VALUES (?,?,?,?)",
                        [docMedico,fecha,hora,estado])
            connection.commit()

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
