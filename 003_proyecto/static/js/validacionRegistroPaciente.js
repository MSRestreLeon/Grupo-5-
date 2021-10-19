// https://www.w3schools.com/js/js_validation.asp
function validarDatos() {
    let nombres = document.forms["formRegistroPaciente"]["nombres"].value;
    let id = document.forms["formRegistroPaciente"]["id"].value;
    let edad = document.forms["formRegistroPaciente"]["edad"].value;
    let profesion = document.forms["formRegistroPaciente"]["profesion"].value;
    let email = document.forms["formRegistroPaciente"]["email"].value;
    let genero = document.forms["formRegistroPaciente"]["genero"].value;
    let tipoSangre = document.forms["formRegistroPaciente"]["tipoSangre"].value;
    let password = document.forms["formRegistroPaciente"]["password"].value;
    let confirmarPassword = document.forms["formRegistroPaciente"]["confirmarPassword"].value;

    if (nombres === '' || id === '' || edad === '' ||
        profesion === '' || email === '' || genero === 'noValido' ||
        tipoSangre === 'noValido' || password === '' || confirmarPassword === '') {
        alert(' [ERROR] Existen campos en blanco o que no se han seleccionado')
    }

    if (!email.includes("@")) {
        alert("[ERROR] Debe ingresar un correo válido que contenga @")
    }

    if (password != confirmarPassword) {
        alert('[ERROR] Las contraseñas ingresadas no coinciden');
    }

    if (password.length < 8 || confirmarPassword.length < 8) {
        alert('[ERROR] La contraseña debe ser de mínimo 8 caracteres');
    }

    return false
}