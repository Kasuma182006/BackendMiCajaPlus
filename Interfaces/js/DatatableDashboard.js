let tablaHistorial; 

$(document).ready(function(){
    // Inicialización
    tablaHistorial = $('#datos_historial_actividades').DataTable({
        language:{
            url:"https://cdn.datatables.net/plug-ins/1.11.5/i18n/es-ES.json"
        },
        columnDefs: [
            { targets: "_all", className: "dt-center" }
        ],
        columns: [
            { data: "tipo" },
            { data: "mensaje" },
            { 
                data: "fecha",
                render: function(data) {
                    if (!data) return "";
                    const fechaObj = new Date(data);
                    return fechaObj.toLocaleString('es-ES', {
                        day: '2-digit', month: '2-digit', year: 'numeric',
                        hour: '2-digit', minute: '2-digit', hour12: true
                    });
                }
            }
        ]
    });

    cargarHistorial();
});

async function cargarHistorial(fInicial = null, fFinal = null) {
    const cedula = sessionStorage.getItem('cedula_tendero');
    
    // Si fFinal es vacío pero fInicial tiene datos, igualamos para buscar un solo día
    let fFinEnvio = (fInicial && !fFinal) ? fInicial : fFinal;

    console.log("--- DEBUG DATATABLE ---");
    console.log("Enviando a /historialActividades:", { 
        idTendero: cedula, 
        fechaInicial: fInicial, 
        fechaFin: fFinEnvio 
    });

    try {
        const res = await fetch(`http://127.0.0.1:4000/historialActividades`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                idTendero: cedula,
                fechaInicial: fInicial, 
                fechaFin: fFinEnvio
            })
        });

        if (!res.ok) throw new Error("Error en la respuesta del servidor");

        const data = await res.json();

        console.log("Respuesta del Servidor (Data):", data);
        console.log("Datos recibidos del historial:", data);

        if (tablaHistorial) {
            tablaHistorial.clear().rows.add(data).draw();
            console.log("Tabla dibujada con éxito");
        }
    } catch (e) {
        console.error("Error cargando historial:", e);
    }
}

//muestra el menu
function mostrarMenu(){ 
    const btn_menu = document.getElementById("btn_menu");
    const ops_menu = document.getElementById("menu_opciones");

    btn_menu.addEventListener("click", ()=>{
        if (ops_menu.style.display == "flex"){
            ops_menu.style.display = "none";
        }else{
            ops_menu.style.display = "flex";
        }
    });
}

document.addEventListener("DOMContentLoaded", ()=>{
    if (document.querySelector("#menu_opciones")){
        mostrarMenu();
    }
});

//muestra la gráfica
var ctx = document.getElementById('myChart').getContext('2d');
window.myChart = new Chart(ctx,{
    type:'bar',
    data:{
        labels:['Ventas','Costos','Gastos','Créditos'],
        datasets:[{
            data:[0,0,0,0],
            backgroundColor:['#D0EFFF','#E0E7FF','#FFDADA','#FEF3C7']
        }]
    },
    options:{responsive:true}
});