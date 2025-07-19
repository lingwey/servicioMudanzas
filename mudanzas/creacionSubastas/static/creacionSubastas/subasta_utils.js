console.log("subasta_utils.js cargado correctamente");

function formatearMoneda(valor) {
    return "$" + parseFloat(valor).toLocaleString("es-AR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function obtenerHoraLegible(fechaStr) {
    const fecha = new Date(fechaStr);
    return fecha.toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit" });
}
