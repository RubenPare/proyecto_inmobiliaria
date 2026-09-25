// Captura el submit del formulario de búsqueda
document.getElementById('form-buscar').addEventListener('submit', function (e) {
    e.preventDefault();

    const termino = document.getElementById('input-buscar').value.trim();

    if (termino === '') {
        alert('Ingresá una ubicación o tipo de propiedad para buscar.');
        return;
    }

    // TODO: reemplazar por una llamada real al backend (ej: /api/propiedades?q=termino)
    // cuando se conecte la búsqueda a la base de datos.
    console.log('Buscando:', termino);
    alert('Buscando propiedades para: "' + termino + '"');
});
