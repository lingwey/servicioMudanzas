console.log("subasta.js cargado correctamente");
function actualizarOfertas(subastaId) {
    fetch(`/subastas/ofertas-ajax/${subastaId}/`)
        .then(response => response.json())
        .then(data => {
            const contenedor = document.getElementById("ofertas-container");
            if (contenedor) {
                contenedor.innerHTML = data.html;
            }
        });
}

function iniciarActualizacion(subastaId, intervalo = 5000) {
    setInterval(() => actualizarOfertas(subastaId), intervalo);
}