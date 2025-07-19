console.log("subasta_ui.js cargado correctamente");

function animarNuevaOferta() {
    const contenedor = document.getElementById("ofertas-container");
    if (contenedor) {
        contenedor.classList.add("destacar-oferta");
        setTimeout(() => contenedor.classList.remove("destacar-oferta"), 1000);
    }
}

