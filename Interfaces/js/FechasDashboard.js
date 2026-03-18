$(document).ready(function(){

    const hoy = new Date().toISOString().split("T")[0];

    // Se limita fechas máximas al día de hoy
    $("#fecha_inicial").attr("max", hoy);
    $("#fecha_final").attr("max", hoy);

});


$("#fecha_inicial").on("change", function(){

    const fecha = $(this).val();

    $("#fecha_final").val(fecha);

});

/* ENVÍO DEL FORMULARIO */
$("form").on("submit", async function(e){
    e.preventDefault();

    $("#menu_opciones").hide();

    const fechaInicial = $("#fecha_inicial").val();
    const fechaFinal   = $("#fecha_final").val();
    const idTendero = sessionStorage.getItem('cedula_tendero');

    const hoy = new Date().toISOString().split("T")[0];

    if(!fechaInicial){
        alert("Por favor, selecciona al menos la fecha inicial.");
        return;
    }

    // Validaciones
    if(fechaInicial > hoy){
        alert("No puedes seleccionar una fecha futura.");
        return;
    }

    if(fechaFinal && fechaFinal > hoy){
        alert("La fecha final no puede ser mayor a hoy.");
        return;
    }

    try {

        const res = await fetch(`http://127.0.0.1:4000/reportePorRango`, {

            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                idTendero: idTendero,
                fechaInicio: fechaInicial,
                fechaFin: fechaFinal || hoy
            })
        });

        const data = await res.json();

        console.log("Datos recibidos para Tarjetas/Gráfica:", data);

        // TARJETAS
        pintarTarjetas({
            ventas: data.total_ventas,
            costos: data.total_costos,
            gastos: data.total_gastos,
            valorCredito: data.total_creditos
        });

        pintarUtilidad(data.total_ventas, data.total_costos, data.total_gastos);

        // GRÁFICA
        if(window.myChart){

            myChart.data.datasets[0].data = [
                data.total_ventas || 0,
                data.total_costos || 0,
                data.total_gastos || 0,
                data.total_creditos || 0
            ];

            myChart.data.datasets[0].label =
            `Reporte del ${fechaInicial} al ${fechaFinal || hoy}`;

            myChart.update();
        }

        const fechaFinConsulta = fechaFinal || fechaInicial;
        cargarHistorial(fechaInicial, fechaFinConsulta);

        console.log({
            fechaInicial: fechaInicial,
            fechaFinal: fechaFinConsulta
        });

    } catch (error) {

        console.error("Error:", error);

    }
    
});

/* BOTÓN QUITAR FILTROS */
$(".btn-quitar-filtros").on("click", function(e){

    e.preventDefault();

    $("#fecha_inicial").val('');
    $("#fecha_final").val('');

    // recargar historial
    cargarHistorial();

    // recargamos tarjetas
    if(typeof cargarEstadisticasHoy === "function"){

        cargarEstadisticasHoy();

    }else{

        location.reload();

    }

});