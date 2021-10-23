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
    agendaHoras=[""]
    agendaId=[""]
    agendaHorasStr=""
    agendaIdStr=""
    if request.method == 'POST':
        fechaAgenda = request.form["fechaAgenda"]
        docMedico = request.form["docMedico"]
        #Consultar y mostrar
        with sqlite3.connect("hospital.db") as connection:
            # Lugar donde almacenamos todo lo que vamos a ejecutar
            cursor = connection.cursor()
            cursor.execute(
                "SELECT count(*) FROM agendaMedica WHERE idMedico = ? AND fecha = ?",
                [docMedico,fechaAgenda])
            matriz = cursor.fetchall()
            tamañoMatriz=matriz[0][0]
            cursor.execute(
                "SELECT * FROM agendaMedica WHERE idMedico = ? AND fecha = ?",
                [docMedico,fechaAgenda])
            matriz2 = cursor.fetchall()
            for i in range(tamañoMatriz):
                agendaHoras.append(matriz2[i][3]) 
            for i in range(tamañoMatriz):
                agendaId.append(str(matriz2[i][0]))
            agendaHorasStr = " Hora : ".join(agendaHoras)
            agendaIdStr = " Id cita: ".join(agendaId)
    return render_template("medico.html",agendaHorasStr=agendaHorasStr,agendaIdStr=agendaIdStr)


@app.route("/medico/historiaClinica", methods=["GET", "POST"])
def historia_clinica():
    historia=''
    historiaMatriz=[]
    if request.method == 'POST':
        docPaciente = request.form["docPaciente"]
        # Consultar y mostrar
        with sqlite3.connect("hospital.db") as connection:
            # Lugar donde almacenamos todo lo que vamos a ejecutar
            cursor = connection.cursor()
            cursor.execute(
                "SELECT count(*) FROM historiaClinica WHERE docPaciente = ? ",
                [docPaciente])
            matriz = cursor.fetchall()
            tamañoMatriz=matriz[0][0]
            cursor.execute("SELECT * FROM historiaClinica WHERE docPaciente = ? ",
                [docPaciente])
            matriz2 = cursor.fetchall()
            for i in range(tamañoMatriz):
                d = matriz2[i][1]
                historiaMatriz.append("Consulta con id de cita ( %d ) : " %d)
                for c in range(18):
                    if c == 0 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append("/Id historia clinica: ")
                        historiaMatriz.append(str(matriz2[i][c])) 
                    if c == 2 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Sintomas: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 3 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Antecedentes: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 4 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Cirugias: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 5 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Diagnostico: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 6 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Examenes medicos: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 7 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Peso: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 8 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /altura: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 9 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Presion Arterial: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 10 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Temperatura: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 11 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Farmacologia: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 12 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Parejas: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 13 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Embarazo: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 14 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Nacidos vivos: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 15 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Parto Natural: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 16 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Metodo Anticonceptivo: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 17 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Drogas: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                    if c == 18 and (matriz2[i][c]=="")==False:
                        historiaMatriz.append(" /Orden Medica: ")
                        historiaMatriz.append(str(matriz2[i][c]))
                historiaMatriz.append("---------------------")
            historia = "  ".join(historiaMatriz)
            
        
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
    return render_template("consultaMedica.html",mensaje=mensaje)

# Rutas Super Administrador


@app.route("/superAdministrador", methods=["GET", "POST"])
def superAdministrador():
    return render_template("superAdministrador.html")

@app.route("/superAdministrador/editarMedico", methods=["GET", "POST"])
def editarMedico():
    if request.method == 'POST':
        docMedicoOriginal = request.form["docMedicoOriginal"]
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
                cursor.execute("UPDATE medico  SET id = (?) where id = (?) ",
                        [docMedico,docMedicoOriginal])
                cursor.execute("UPDATE usuario  SET id = (?) where id = (?) and rol='medico'",
                        [docMedico,docMedicoOriginal])
                cursor.execute("UPDATE agendaMedica  SET idMedico = (?) where idMedico = (?)",
                        [docMedico,docMedicoOriginal])
                cursor.execute("UPDATE citaMedica  SET idMedico = (?) where idMedico = (?)",
                        [docMedico,docMedicoOriginal])
                connection.commit()
            if (especialidad==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("UPDATE medico SET especialidad = (?) where id = (?)",
                        [especialidad,docMedicoOriginal])
                connection.commit()
            if (estado==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("UPDATE usuario  SET estado = (?) where id = (?) and rol='medico'",
                        [estado,docMedicoOriginal])
                connection.commit()
    return render_template("editarMedico.html")

@app.route("/superAdministrador/dashboard", methods=["GET", "POST"])
def superAdministradorDashboard():
    return render_template("dashboard.html")

@app.route("/superAdministrador/editarPaciente", methods=["GET", "POST"])
def superAdministradorEditarPaciente():
    if request.method == 'POST':
        idOrigal = request.form["idOriginal"]
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
            if (id==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("UPDATE paciente SET id = (?) where id = (?)",
                        [id,idOrigal])
                cursor.execute("UPDATE usuario SET id = (?) where id = (?)",
                        [id,idOrigal])
                cursor.execute("UPDATE historiaClinica SET docPaciente = (?) where docPaciente = (?)",
                        [id,idOrigal])
                cursor.execute("UPDATE citaMedica SET idPaciente = (?) where idPaciente = (?)",
                        [id,idOrigal])
                connection.commit()

            if (edad==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("UPDATE paciente SET edad = (?) where id = (?)",
                        [edad,idOrigal])
                connection.commit()
            
            if (profesion==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("UPDATE paciente SET profesion = (?) where id = (?)",
                        [profesion,idOrigal])
                connection.commit()
            
            if (email==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("UPDATE paciente SET email = (?) where id = (?)",
                        [email,idOrigal])
                connection.commit()
            if (genero==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("UPDATE paciente SET genero = (?) where id = (?)",
                        [genero,idOrigal])
                connection.commit()

            if (rh==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("UPDATE paciente SET tipoSangre = (?) where id = (?)",
                        [rh,idOrigal])
                connection.commit()

            if (estado==""):
                mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
            else:
                cursor.execute("UPDATE usuario SET estado = (?) where id = (?)",
                        [estado,idOrigal])
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
            #cursor = connection.cursor()
            #cursor.execute("SELECT * FROM agendaMedica WHERE idMedico=? and fecha=? and hora=? and estado=? ",
            #        [docMedico,fecha,hora,estado])
            #matriz = cursor.fetchall()
            #idCita=matriz[0][0]
            #cursor.execute("INSERT INTO citaMedica (idAgendaMedica) VALUES (?)",
            #            [idCita])
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
