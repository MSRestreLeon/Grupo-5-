function validarDatosAgendaCita() {
    let fechaAgendaCita = document.getElementById("fechaAgendaCita").value;
    let horaAgendaCita = document.getElementById("horaAgendaCita").value;

    if (fechaAgendaCita === '' || horaAgendaCita === '') {
        alert('Para listar las citas disponibles y solicitar una cita es necesario no dejar campos en blanco')
    }
}

function validarDatosCitasPasadas() {
    let fechaInicialCitaPasada = document.getElementById("fechaInicialCitaPasada").value;
    let fechaFinalCitaPasada = document.getElementById("fechaFinalCitaPasada").value;

    if (fechaInicialCitaPasada === '' || fechaFinalCitaPasada === '' || fechaInicialCitaPasada > fechaFinalCitaPasada) {
        alert('Para ver las citas pasadas es necesario no dejar campos en blanco y que la fecha final no sea anterior a la fecha inicial')
    }
}