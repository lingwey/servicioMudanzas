console.log("subasta_ws.js cargado correctamente");

const subastaId = window.subastaId;  // Asegurate de exponer esto en tu template
const ws_url = `ws://${window.location.host}/ws/subasta/${subastaId}/`;

const socket = new WebSocket(ws_url);

socket.onopen = () => {
    console.log("Conectado al WebSocket de la subasta " + subastaId);
};

socket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    if (data.tipo === "nueva_oferta") {
        const contenedor = document.getElementById("ofertas-container");
        if (contenedor) {
            contenedor.innerHTML = data.html;
            animarNuevaOferta();  // llamada a UI
        }
    }
};

socket.onerror = (e) => console.error("Error en WebSocket", e);
socket.onclose = () => console.log("WebSocket cerrado.");
