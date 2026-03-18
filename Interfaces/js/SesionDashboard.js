async function cargarSesion(){
    try{
        const res = await fetch(`http://127.0.0.1:4000/sesion`, {
            credentials: 'include'
        });

        const data = await res.json();

        if(data.logueado){
            document.getElementById('nombre_tendero').textContent = data.nombre;
        }else{
            window.location.href = "InicioSesion.html";
        }

    }catch(e){
        console.error(e);
    }
}

document.addEventListener('DOMContentLoaded', cargarSesion);