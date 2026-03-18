// -------- FORMATO MONEDA COP --------
function formatoCOP(valor){
    return valor.toLocaleString('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    });
}

// -------- PINTAR TARJETAS --------
function pintarTarjetas(data){
    
    document.querySelector('#ventas .valor').textContent  = `${formatoCOP(Math.abs(data.ventas || 0))}`;
    document.querySelector('#costos .valor').textContent  = `${formatoCOP(Math.abs(data.costos || 0))}`;
    document.querySelector('#gastos .valor').textContent  = `${formatoCOP(Math.abs(data.gastos || 0))}`;
    document.querySelector('#credito .valor').textContent = `${formatoCOP(Math.abs(data.valorCredito || 0))}`;
}

// -------- UTILIDAD --------
function pintarUtilidad(ventas, costos, gastos){
    const utilidadEl = document.querySelector('#utilidad .valor');
    const tarjetaEl  = document.getElementById('utilidad');

    const utilidad = (ventas || 0) - (costos || 0) - (gastos || 0);

    utilidadEl.classList.remove('utilidad-positiva','utilidad-negativa');
    tarjetaEl.classList.remove('utilidad-positiva','utilidad-negativa');

    if(utilidad >= 0){
        utilidadEl.textContent = formatoCOP(utilidad);
        utilidadEl.classList.add('utilidad-positiva');
        tarjetaEl.classList.add('utilidad-positiva');
    } else {
        utilidadEl.textContent = `− ${formatoCOP(Math.abs(utilidad))}`;
        utilidadEl.classList.add('utilidad-negativa');
        tarjetaEl.classList.add('utilidad-negativa');
    }
}

// -------- MOSTRAR NOMBRE --------
function mostrarNombreTendero() {
    const nombre = sessionStorage.getItem('nombre_tendero'); 
    const spanNombre = document.getElementById('nombre_tendero');
    
    if (nombre && spanNombre) {
        spanNombre.textContent = nombre;
    } else {
        console.warn("Sesión no encontrada, redirigiendo...");
        window.location.href = "InicioSesion.html"; 
    }
}

// -------- CARGAR RESUMEN DEL DÍA --------
async function cargarResumenHoy(){
    mostrarNombreTendero();

    const cedula = sessionStorage.getItem('cedula_tendero'); 

    try {
        const res = await fetch(`http://127.0.0.1:4000/consultarEstadisticas`,{
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({
                idTendero: cedula,
            })
        });

        const data = await res.json();

        pintarTarjetas(data);
        pintarUtilidad(data.ventas, data.costos, data.gastos);

        if(window.myChart){
            myChart.data.datasets[0].data = [
                data.ventas || 0,
                data.costos || 0,
                data.gastos || 0,
                data.valorCredito || 0
            ];
                myChart.data.datasets[0].label = `Hoy`;

                myChart.update();
        }

    } catch (error) {
        console.error("Error cargando estadísticas:", error);
    }
}

document.addEventListener('DOMContentLoaded', cargarResumenHoy);
// -------- CERRAR SESIÓN --------
function cerrarSesion(){
    const confirmar = confirm("¿Seguro que deseas cerrar sesión?");
    
    if(confirmar){
        sessionStorage.clear(); 
        window.location.href = "InicioSesion.html";
    }
}

// Evento al icono de cerrar
document.addEventListener("DOMContentLoaded", () => {
    const btnCerrar = document.getElementById("opcion_cerrar");
    
    if(btnCerrar){
        btnCerrar.addEventListener("click", cerrarSesion);
    }
});