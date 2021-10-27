from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import hashlib
import os

app = Flask(import_name=__name__)

app.secret_key = os.urandom(24)

# Login

@app.route("/", methods=["GET", "POST"])
def login():
    # Especifica la variable mensaje
    mensaje = ''

    # Se setea en blanco los datos para cerrar sesion
    if request.method == 'GET':
        id = ""
        rol = ""
        session["id"] = id
        session["rol"] = rol

    if request.method == 'POST':
        # Las variables se obtinen a través del
        # atributo name en cada elemento
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

#Ruta registro paciente

@app.route("/registroPaciente", methods=['GET', 'POST'])
def registroPaciente():
    mensaje=''
    mensajep=''
    if request.method == 'POST':
        nombres = request.form["nombres"]
        id = request.form["id"]
        edad = request.form["edad"]
        profesion = request.form["profesion"]
        email = request.form["email"]
        genero = request.form["genero"]
        tipoSangre = request.form["tipoSangre"]
        password = request.form["password"]
        password2 = request.form["password2"]
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
            cursor.execute("SELECT count(*) FROM paciente WHERE id = ? ",
                [id])
            validadorMatriz = cursor.fetchall()
            validador=validadorMatriz[0][0]
            if validador == 0 and nombres != "" and id != "" and edad != "" and profesion != "" and email != "" and genero != "" and tipoSangre != "" and password==password2:
                cursor.execute("INSERT INTO usuario VALUES (?, ?, ?, ?, ?)",
                               [id, nombres, rol, passwordEncode, estado])
                cursor.execute("INSERT INTO paciente VALUES (?, ?, ?, ?, ?, ?)",
                               [id, edad, profesion, email, genero, tipoSangre])
                connection.commit()
                mensajep='Registro exitoso'
            else:mensaje='[ERROR]Favor revise los datos ingresados, operacion abortada'
    return render_template("registroPaciente.html",mensaje=mensaje,mensajep=mensajep)


#@app.route("/recuperarContrasena", methods=["GET", "POST"])
#def recuperarContrasena():
#    return render_template("recuperarContrasena.html")
#
#
#@app.route("/generarNuevaContrasena")
#def generarNuevaContrasena():
#    return render_template("generarNuevaContrasena.html")

#Ruta principal paciente
@app.route("/paciente")
def paciente():
    vSesion=''
    # En esta parte recuerde que la sesión es como un diccionario
    # Es decir si la llave se encuentra en el diccionario entonces
    # se obtiene true
    if 'id' in session and session["rol"] == 'paciente' :
        return render_template("paciente.html")
    #En caso de no logiarse el usuario se muestra el mensaje en el login
    else:
        vSesion='Inicie sesion para poder ingresar a la plataforma' 
        return render_template("login.html",vSesion=vSesion)

#Ruta cita medica desde paciente
@app.route("/paciente/citaMedica", methods=["GET", "POST"])
def citaMedica():
    citasDisponibles=''
    hora=''
    mensaje=''
    mensajep=''
    vSesion=''
    if 'id' in session and session["rol"] == 'paciente':
        if  (request.method == 'POST'):
            fecha = request.form["fecha"]
            idCitaSolicitada = request.form["idCitaSolicitada"]
            idPaciente=request.form["idPaciente"]
            idCitaCalificar=request.form["idCitaCalificarn"]
            calificacion=request.form["calificacion"]
            agendaHoras=[""]
            agendaId=[""]
            with sqlite3.connect("hospital.db") as connection:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                if (fecha=="")==False :
                    cursor.execute("SELECT count(*) FROM agendaMedica WHERE fecha = ? and estado='disponible' ",
                                    [fecha])
                    validadorMatriz = cursor.fetchall()
                    validador=validadorMatriz[0][0]
                    if validador>0:
                        cursor.execute("SELECT count(*) FROM agendaMedica WHERE estado = 'disponible' AND fecha = ? ",
                                       [fecha])
                        matriz = cursor.fetchall()
                        tamañoMatriz=matriz[0][0]
                        cursor.execute("SELECT * FROM agendaMedica WHERE estado = 'disponible' AND fecha = ? ",
                                       [fecha])
                        matriz2 = cursor.fetchall()
                        for i in range(tamañoMatriz):
                            agendaHoras.append(matriz2[i][3]) 
                        for i in range(tamañoMatriz):
                            agendaId.append(str(matriz2[i][0]))
                        hora = " Hora : ".join(agendaHoras)
                        citasDisponibles = " Id cita: ".join(agendaId)
                    else:mensaje='[ERROR]La fecha ingresada no se encuentra disponible, operacion abortada'
                if (idCitaSolicitada=="")==False and (idPaciente=="")==False:
                    cursor.execute("SELECT count(*) FROM agendaMedica WHERE id = ? and estado='disponible' ",
                                    [idCitaSolicitada])
                    validadorMatriz1 = cursor.fetchall()
                    validador1=validadorMatriz1[0][0]
                    cursor.execute("SELECT count(*) FROM paciente WHERE id = ? ",
                                    [idPaciente])
                    validadorMatriz2 = cursor.fetchall()
                    validador2=validadorMatriz2[0][0]
                    estadoAgenda="noDisponible"
                    estadoCita="pendiente"
                    if validador1>0:
                        if validador2>0:
                            cursor.execute("UPDATE agendaMedica SET estado = (?) where id = (?)",
                                    [estadoAgenda,idCitaSolicitada])
                            cursor.execute("SELECT idMedico FROM agendaMedica WHERE id = ?  ",
                                    [idCitaSolicitada])
                            matriz = cursor.fetchall()
                            idMedico=matriz[0][0]
                            cursor.execute("INSERT INTO citaMedica (idAgendaMedica, idPaciente, idMedico, estado)VALUES (?, ?, ?, ?)",
                                    [idCitaSolicitada, idPaciente, idMedico, estadoCita])
                        else:mensaje='[ERROR]El documento de identidad ingresado no existe, operacion abortada'
                    else:mensaje='[ERROR]El id de la cita que desea agendar no existe o no se encuentra disponible, operacion abortada'
                if (idCitaCalificar=="")==False:
                    cursor.execute("SELECT count(*) FROM citaMedica WHERE idAgendaMedica = ? and estado='cumplida'",
                                    [idCitaCalificar])
                    validadorMatriz3 = cursor.fetchall()
                    validador3=validadorMatriz3[0][0]
                    if validador3>0:
                        cursor.execute("UPDATE citaMedica SET calificacion = (?) where idAgendaMedica = (?)",
                                [calificacion,idCitaCalificar])
                        mensajep='Cita calificada exitosamente, gracias por calificar nuestros servicios'
                    else: mensaje='[ERROR]La cita ingresada no esta disponible para ser evaluada, operacion abortada'
        return render_template("citaMedica.html",hora=hora,citasDisponibles=citasDisponibles,mensaje=mensaje,mensajep=mensajep)
    else:
        vSesion='Inicie sesion para poder ingresar a la plataforma' 
        return render_template("login.html",vSesion=vSesion)

#Ruta examen medico desde paciente
@ app.route("/paciente/examenMedico", methods=["GET", "POST"])
def examenMedico():
    examenes=''
    mensaje=''
    vSesion=''
    if 'id' in session and session["rol"] == 'paciente':
        if  (request.method == 'POST'):
            idPaciente = request.form["idPaciente"]
            matrizExamenes=[]
            
            with sqlite3.connect("hospital.db") as connection:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                cursor.execute("SELECT count(*) FROM paciente WHERE id = ? ",
                    [idPaciente])
                validadorMatriz = cursor.fetchall()
                validador=validadorMatriz[0][0]
                if validador==1: 
                    cursor.execute(
                        "SELECT count(*) FROM historiaClinica WHERE docPaciente = ? ",
                                    [idPaciente])
                    matriz = cursor.fetchall()
                    tamañoMatriz=matriz[0][0]
                    cursor.execute("SELECT * FROM historiaClinica WHERE docPaciente = ?",
                                   [idPaciente])
                    matriz2 = cursor.fetchall()
                    for i in range(tamañoMatriz):
                        matrizExamenes.append(matriz2[i][7])
                    examenes = "  ".join(matrizExamenes)
                else:mensaje='Documento de identidad no encontrado'
        return render_template("examenMedico.html",examenes=examenes,mensaje=mensaje)
    else:
        vSesion='Inicie sesion para poder ingresar a la plataforma' 
        return render_template("login.html",vSesion=vSesion)

#Ruta historia clinica desde paciente
@ app.route("/paciente/historiaClinica", methods=["GET", "POST"])
def pacienteHistoriaClinica():
    historia=''
    historiaMatriz=[]
    mensaje=''
    vSesion=''
    if 'id' in session and session["rol"] == 'paciente':
        if  request.method == 'POST':
            docPaciente = request.form["docPaciente"]
            # Consultar y mostrar
            with sqlite3.connect("hospital.db") as connection:
                # Lugar donde almacenamos todo lo que vamos a ejecutar
                cursor = connection.cursor()
                cursor.execute("SELECT count(*) FROM paciente WHERE id = ? ",
                                   [docPaciente])
                validadorMatriz = cursor.fetchall()
                validador=validadorMatriz[0][0]
                if validador==1:
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
                        for c in range(20):
                            if c == 0 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append("/Id historia clinica: ")
                                historiaMatriz.append(str(matriz2[i][c])) 
                            if c == 3 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Sintomas: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 4 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Antecedentes: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 5 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Cirugias: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 6 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Diagnostico: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 7 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Examenes medicos: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 8 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Peso: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 9 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /altura: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 10 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Peresion Arterial: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 11 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Temperatura: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 12 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Farmacologia: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 13 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Parejas: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 14 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Embarazo: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 15 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Nacidos vivos: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 16 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Parto Natural: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 17 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Metodo Anticonceptivo: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 18 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Drogas: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 19 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Orden Medica: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                        historiaMatriz.append("---------------------")
                    historia = "  ".join(historiaMatriz)
                else: mensaje='[ERROR]Documento de identidad no encontrado'
        return render_template("pacienteHistoriaClinica.html",historia=historia,mensaje=mensaje)
    else:
        vSesion='Inicie sesion para poder ingresar a la plataforma' 
        return render_template("login.html",vSesion=vSesion)

# Ruta principal medico

@app.route("/medico", methods=["GET", "POST"])
def medico():
    agendaHoras=[""]
    agendaId=[""]
    agendaHorasStr=""
    agendaIdStr=""
    mensaje=""
    vSesion=''
    if 'id' in session and session["rol"] == 'medico':
        if  request.method == 'POST':
            fechaAgenda = request.form["fechaAgenda"]
            docMedico = request.form["docMedico"]
            #Consultar y mostrar
            with sqlite3.connect("hospital.db") as connection:
                # Lugar donde almacenamos todo lo que vamos a ejecutar
                cursor = connection.cursor()
                cursor.execute("SELECT count(*) FROM agendaMedica WHERE fecha = ? and idMedico = ? ",
                    [fechaAgenda,docMedico])
                validadorMatriz = cursor.fetchall()
                validador=validadorMatriz[0][0]
                if validador>0:
                    cursor.execute(
                        "SELECT count(*) FROM agendaMedica WHERE idMedico = ? AND fecha = ? AND estado = 'noDisponible'",
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
                else:mensaje='[Error]Favor revise los datos ingresados, operacion abortada'
        return render_template("medico.html",agendaHorasStr=agendaHorasStr,agendaIdStr=agendaIdStr,mensaje=mensaje)
    else:
        vSesion='Inicie sesion para poder ingresar a la plataforma' 
        return render_template("login.html",vSesion=vSesion)

#Ruta historia clinica desde medico

@app.route("/medico/historiaClinica", methods=["GET", "POST"])
def historia_clinica():
    historia=''
    historiaMatriz=[]
    mensaje=''
    vSesion=''
    if 'id' in session and session["rol"] == 'medico':
        if request.method == 'POST':
            docPaciente = request.form["docPaciente"]
            # Consultar y mostrar
            with sqlite3.connect("hospital.db") as connection:
                # Lugar donde almacenamos todo lo que vamos a ejecutar
                cursor = connection.cursor()
                cursor.execute("SELECT count(*) FROM paciente WHERE id = ? ",
                    [docPaciente])
                validadorMatriz = cursor.fetchall()
                validador=validadorMatriz[0][0]
                if validador==1: 
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
                        for c in range(20):
                            if c == 0 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append("/Id historia clinica: ")
                                historiaMatriz.append(str(matriz2[i][c])) 
                            if c == 3 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Sintomas: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 4 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Antecedentes: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 5 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Cirugias: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 6 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Diagnostico: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 7 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Examenes medicos: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 8 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Peso: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 9 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /altura: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 10 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Presion Arterial: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 11 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Temperatura: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 12 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Farmacologia: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 13 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Parejas: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 14 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Embarazo: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 15 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Nacidos vivos: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 16 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Parto Natural: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 17 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Metodo Anticonceptivo: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 18 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Drogas: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                            if c == 19 and (matriz2[i][c]=="")==False:
                                historiaMatriz.append(" /Orden Medica: ")
                                historiaMatriz.append(str(matriz2[i][c]))
                        historiaMatriz.append("---------------------")
                    historia = "  ".join(historiaMatriz)
                else:mensaje='[ERROR]Documento de identidad no encontrado, operacion abortada'
        return render_template("historiaClinica.html",historia=historia,mensaje=mensaje)
    else:
        vSesion='Inicie sesion para poder ingresar a la plataforma' 
        return render_template("login.html",vSesion=vSesion)

#Ruta consulta medica desde medico
@app.route("/medico/consultaMedica", methods=["GET", "POST"])
def consulta_medica():
    mensaje = ''
    mensaje2 = ''
    mensajep = ''
    vSesion=''
    if 'id' in session and session["rol"] == 'medico':
        if  request.method == 'POST':
            idCita = request.form["idCita"]
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
            estado = 'cumplida'
            # Consultar y mostrar
            with sqlite3.connect("hospital.db") as connection:
                # Lugar donde almacenamos todo lo que vamos a ejecutar
                cursor = connection.cursor()
                cursor.execute("SELECT count(*) FROM citaMedica WHERE idAgendaMedica = ? and idPaciente = ?",
                    [idCita,docPaciente])
                validadorMatriz = cursor.fetchall()
                validador=validadorMatriz[0][0]
                if validador:
                    if idCita == "" or docPaciente == "" or sintomas == "" or antecedentes == "" or cirugias == "" or diagnostico == "" or examenesMedicos == "" or peso == "" or altura == "" or precionArterial == "" or parejas == "" or ordenMedicamentos == "":
                        mensaje="[ERROR]Ingrese los datos obligatorios de la consulta medica (*), operacion abortada"
                    else:
                        cursor.execute(
                        "UPDATE citaMedica  SET estado = (?) where idAgendaMedica = (?) ",
                        [estado,idCita])
                        cursor.execute("INSERT INTO historiaClinica (idConsulta,docPaciente,sintomas,antecedentes,cirugias,diagnostico,examenesMedicos,peso,altura,presionArterial,temperatura,farmacologia,parejas,embarazos,nacidosVivos,partoNatural,metodoAnticonceptivo,drogas,ordenMedicamentos) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                   [idCita,docPaciente,sintomas,antecedentes,cirugias,diagnostico,examenesMedicos,peso,altura,precionArterial,temperatura,farmacologia,parejas,embarazos,nacidosVivos,partoNatural,metodoAnticonceptivo,drogas,ordenMedicamentos])
                        connection.commit()
                        mensajep='Consulta cargada exitosamente'
                else:mensaje2='[ERROR]Favor verifique los datos identificadores de la consulta, operacion abortada'
        return render_template("consultaMedica.html",mensajep=mensajep,mensaje=mensaje,mensaje2=mensaje2)
    else:
        vSesion='Inicie sesion para poder ingresar a la plataforma' 
        return render_template("login.html",vSesion=vSesion)

# Ruta principal Super Administrador
@app.route("/superAdministrador", methods=["GET", "POST"])
def superAdministrador():
    vSesion=''
    if 'id' in session and session["rol"] == 'superadministrador':
        nombres = session["nombres"]
        return render_template("superAdministrador.html")
    else:
        vSesion='Inicie sesion para poder ingresar a la plataforma' 
        return render_template("login.html",vSesion=vSesion)

#Ruta editar medico desde super administrador
@app.route("/superAdministrador/editarMedico", methods=["GET", "POST"])
def editarMedico():
    mensaje=''
    mensajep=''
    vSesion=''
    if 'id' in session and session["rol"] == 'superadministrador':
        if  request.method == 'POST':
            docMedicoOriginal = request.form["docMedicoOriginal"]
            docMedico = request.form["docMedico"]
            especialidad = request.form["especialidad"]
            estado = request.form["estado"]
            # Consultar y mostrar
            with sqlite3.connect("hospital.db") as connection:
                # Lugar donde almacenamos todo lo que vamos a ejecutar
                cursor = connection.cursor()
                cursor.execute("SELECT count(*) FROM medico WHERE id = ? ",
                    [docMedico])
                validadorMatriz = cursor.fetchall()
                validador=validadorMatriz[0][0]
                if validador>0:
                    if (docMedico==""):
                        mensaje2="Ingrese los datos obligatorios de la consulta medica (*)"
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
                        mensajep='Medico actualizado'
                    if (especialidad==""):
                        mensaje2="Ingrese los datos obligatorios de la consulta medica (*)"
                    else:
                        cursor.execute("UPDATE medico SET especialidad = (?) where id = (?)",
                                [especialidad,docMedicoOriginal])
                        connection.commit()
                        mensajep='Medico actualizado'
                    if (estado==""):
                        mensaje2="Ingrese los datos obligatorios de la consulta medica (*)"
                    else:
                        cursor.execute("UPDATE usuario  SET estado = (?) where id = (?) and rol='medico'",
                                [estado,docMedicoOriginal])
                        connection.commit()
                        mensajep='Medico actualizado'
                else:mensaje='[ERROR]El documento de identidad es invalido, operacion abortada'        
        return render_template("editarMedico.html",mensajep=mensajep,mensaje=mensaje)
    else:
        vSesion='Inicie sesion para poder ingresar a la plataforma' 
        return render_template("login.html",vSesion=vSesion)

#Ruta dashboard desde super administrador
@app.route("/superAdministrador/dashboard", methods=["GET", "POST"])
def superAdministradorDashboard():
    citaConsulta=''
    mensaje=''
    vSesion=''
    if 'id' in session and session["rol"] == 'superadministrador':
        if  (request.method == 'POST'):
            citaConsulta = ''
            fecha = request.form["fechaCita"]
            horaCita = request.form["horaCita"]
            idMedico=request.form["idMedico"]
            agendaCitas=[""]
            i=0
            with sqlite3.connect("hospital.db") as connection:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                if (fecha=="")==False and (horaCita=="")==False  :
                    i=1
                    cursor.execute("SELECT count(*) FROM agendaMedica WHERE fecha = ? and hora = ? ",
                                   [fecha,horaCita])
                    matriz = cursor.fetchall()
                    tamañoMatriz=matriz[0][0]
                    cursor.execute("SELECT * FROM agendaMedica WHERE  fecha = ? and hora = ? ",
                                   [fecha,horaCita])
                    matriz2 = cursor.fetchall()
                    if tamañoMatriz==0:
                        mensaje='[ERROR]Favor revise los datos ingresados'
                    for i in range(tamañoMatriz):
                        d = matriz2[i][0]
                        agendaCitas.append("Informacion de cita con id ( %d ) : " %d)
                        for c in range(4):
                            if c == 1 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Documento de identidad de medico: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 2 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Fecha: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 3 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Hora: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 4 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Estado: ")
                                agendaCitas.append(str(matriz2[i][c]))
                        agendaCitas.append("---------------------")
                    citaConsulta = "  ".join(agendaCitas)
                elif (fecha=="")==False and (idMedico=="")==False  :
                    i=1
                    cursor.execute("SELECT count(*) FROM agendaMedica WHERE fecha = ? and idMedico = ? ",
                                   [fecha,idMedico])
                    matriz = cursor.fetchall()
                    tamañoMatriz=matriz[0][0]
                    cursor.execute("SELECT * FROM agendaMedica WHERE  fecha = ? and idMedico = ? ",
                                   [fecha,idMedico])
                    matriz2 = cursor.fetchall()
                    if tamañoMatriz==0:
                        mensaje='[ERROR]Favor revise los datos ingresados'
                    for i in range(tamañoMatriz):
                        d = matriz2[i][0]
                        agendaCitas.append("Informacion de cita con id ( %d ) : " %d)
                        for c in range(4):
                            if c == 1 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Documento de identidad de medico: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 2 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Fecha: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 3 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Hora: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 4 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Estado: ")
                                agendaCitas.append(str(matriz2[i][c]))
                        agendaCitas.append("---------------------")
                    citaConsulta = "  ".join(agendaCitas)
                
                elif (horaCita=="")==False and (idMedico=="")==False  :
                    i=1
                    cursor.execute("SELECT count(*) FROM agendaMedica WHERE hora = ? and idMedico = ? ",
                                   [horaCita,idMedico])
                    matriz = cursor.fetchall()
                    tamañoMatriz=matriz[0][0]
                    cursor.execute("SELECT * FROM agendaMedica WHERE  hora = ? and idMedico = ? ",
                                   [horaCita,idMedico])
                    matriz2 = cursor.fetchall()
                    if tamañoMatriz==0:
                        mensaje='[ERROR]Favor revise los datos ingresados'
                    for i in range(tamañoMatriz):
                        d = matriz2[i][0]
                        agendaCitas.append("Informacion de cita con id ( %d ) : " %d)
                        for c in range(4):
                            if c == 1 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Documento de identidad de medico: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 2 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Fecha: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 3 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Hora: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 4 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Estado: ")
                                agendaCitas.append(str(matriz2[i][c]))
                        agendaCitas.append("---------------------")
                    citaConsulta = "  ".join(agendaCitas)
                elif (horaCita=="")==False  and i==0 :
                    cursor.execute("SELECT count(*) FROM agendaMedica WHERE hora = ? ",
                                   [horaCita])
                    matriz = cursor.fetchall()
                    tamañoMatriz=matriz[0][0]
                    cursor.execute("SELECT * FROM agendaMedica WHERE hora = ? ",
                                   [horaCita])
                    matriz2 = cursor.fetchall()
                    if tamañoMatriz==0:
                        mensaje='[ERROR]Favor revise los datos ingresados'
                    for i in range(tamañoMatriz):
                        d = matriz2[i][0]
                        agendaCitas.append("Informacion de cita con id ( %d ) : " %d)
                        for c in range(4):
                            if c == 1 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Documento de identidad de medico: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 2 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Fecha: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 3 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Hora: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 4 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Estado: ")
                                agendaCitas.append(str(matriz2[i][c]))
                        agendaCitas.append("---------------------")
                    citaConsulta = "  ".join(agendaCitas)
                elif (idMedico=="")==False  and i==0:
                    cursor.execute("SELECT count(*) FROM agendaMedica WHERE idMedico = ? ",
                                   [idMedico])
                    matriz = cursor.fetchall()
                    tamañoMatriz=matriz[0][0]
                    cursor.execute("SELECT * FROM agendaMedica WHERE  idMedico = ? ",
                                   [idMedico])
                    matriz2 = cursor.fetchall()
                    for i in range(tamañoMatriz):
                        d = matriz2[i][0]
                        agendaCitas.append("Informacion de cita con id ( %d ) : " %d)
                        for c in range(4):
                            if c == 1 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Documento de identidad de medico: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 2 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Fecha: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 3 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Hora: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 4 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Estado: ")
                                agendaCitas.append(str(matriz2[i][c]))
                        agendaCitas.append("---------------------")
                    citaConsulta = "  ".join(agendaCitas)
                elif (fecha=="")==False and i==0:
                    
                    cursor.execute("SELECT count(*) FROM agendaMedica WHERE fecha = ? ",
                                   [fecha])
                    matriz = cursor.fetchall()
                    tamañoMatriz=matriz[0][0]
                    cursor.execute("SELECT * FROM agendaMedica WHERE  fecha = ? ",
                                   [fecha])
                    matriz2 = cursor.fetchall()
                    if tamañoMatriz==0:
                        mensaje='[ERROR]Favor revise los datos ingresados'
                    for i in range(tamañoMatriz):
                        d = matriz2[i][0]
                        agendaCitas.append("Informacion de cita con id ( %d ) : " %d)
                        for c in range(4):
                            if c == 1 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Documento de identidad de medico: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 2 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Fecha: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 3 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Hora: ")
                                agendaCitas.append(str(matriz2[i][c]))
                            if c == 4 and (matriz2[i][c]=="")==False:
                                agendaCitas.append(" /Estado: ")
                                agendaCitas.append(str(matriz2[i][c]))
                        agendaCitas.append("---------------------")
                    citaConsulta = "  ".join(agendaCitas)
        return render_template("dashboard.html",citaConsulta=citaConsulta,mensaje=mensaje)
    else:
        vSesion='Inicie sesion para poder ingresar a la plataforma' 
        return render_template("login.html",vSesion=vSesion)

#Ruta editar paciente desde super administrador
@app.route("/superAdministrador/editarPaciente", methods=["GET", "POST"])
def superAdministradorEditarPaciente():
    mensaje2=''
    mensajep=''
    vSesion=''
    if 'id' in session and session["rol"] == 'superadministrador':
        if  request.method == 'POST':
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
                cursor.execute("SELECT count(*) FROM paciente WHERE id = ? ",
                        [idOrigal])
                validadorMatriz = cursor.fetchall()
                validador=validadorMatriz[0][0]
                if validador>0:
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
                        mensajep='Paciente actualizado exitosamente' 
    
                    if (edad==""):
                        mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
                    else:
                        cursor.execute("UPDATE paciente SET edad = (?) where id = (?)",
                                [edad,idOrigal])
                        connection.commit() 
                        mensajep='Paciente actualizado exitosamente' 
    
                    if (profesion==""):
                        mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
                    else:
                        cursor.execute("UPDATE paciente SET profesion = (?) where id = (?)",
                                [profesion,idOrigal])
                        connection.commit()
                        mensajep='Paciente actualizado exitosamente' 
                    if (email==""):
                        mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
                    else:
                        cursor.execute("UPDATE paciente SET email = (?) where id = (?)",
                                [email,idOrigal])
                        connection.commit()
                        mensajep='Paciente actualizado exitosamente' 
    
                    if (genero==""):
                        mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
                    else:
                        cursor.execute("UPDATE paciente SET genero = (?) where id = (?)",
                                [genero,idOrigal])
                        connection.commit()
                        mensajep='Paciente actualizado exitosamente' 
        
                    if (rh==""):
                        mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
                    else:
                        cursor.execute("UPDATE paciente SET tipoSangre = (?) where id = (?)",
                                [rh,idOrigal])
                        connection.commit()
                        mensajep='Paciente actualizado exitosamente' 
        
                    if (estado==""):
                        mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
                    else:
                        cursor.execute("UPDATE usuario SET estado = (?) where id = (?)",
                                [estado,idOrigal])
                        connection.commit()
                        mensajep='Paciente actualizado exitosamente'                                
                else:mensaje2='[ERROR]Documento de identidad invalido, operacion abortada'
        
        return render_template("editarPaciente.html",mensaje2=mensaje2,mensajep=mensajep)
    else:
        vSesion='Inicie sesion para poder ingresar a la plataforma' 
        return render_template("login.html",vSesion=vSesion)

#@app.route("/superAdministrador/historiaClinica", methods=["GET", "POST"])
#def superAdministradorHistoriaClinica():
    
#    return render_template("historiaClinicaSuper.html")

#Ruta apertura agenda desde super administrador
@app.route("/superAdministrador/aperturaAgenda", methods=["GET", "POST"])
def superAdministradorAperturaAgenda():
    mensaje=''
    mensajep=''
    vSesion=''
    if 'id' in session and session["rol"] == 'superadministrador':
        if  request.method == 'POST':
            docMedico = request.form["docMedico"]
            fecha = request.form["fecha"]
            hora = request.form["hora"]
            estado = 'disponible'
            # Consultar y mostrar
            with sqlite3.connect("hospital.db") as connection:
                # Lugar donde almacenamos todo lo que vamos a ejecutar
                cursor = connection.cursor()
                cursor.execute("SELECT count(*) FROM medico WHERE id = ? ",
                    [docMedico])
                validadorMatriz = cursor.fetchall()
                validador=validadorMatriz[0][0]
                if validador>0:
                    if (docMedico=="" or fecha=="" or hora=="" or estado==""):
                        mensaje="Ingrese los datos obligatorios de la consulta medica (*)"
                    else:
                        cursor.execute("INSERT INTO agendaMedica (idMedico,fecha,hora,estado) VALUES (?,?,?,?)",
                                [docMedico,fecha,hora,estado])
                        connection.commit()
                        mensajep='Agenda creada exitosamente'
                else:
                    mensaje='[ERROR]Documento de identidad invalido, operacion abortada'
        return render_template("aperturaAgenda.html",mensaje=mensaje,mensajep=mensajep)
    else:
        vSesion='Inicie sesion para poder ingresar a la plataforma' 
        return render_template("login.html",vSesion=vSesion)

if __name__ == '__main__':
    app.run(debug=True)
