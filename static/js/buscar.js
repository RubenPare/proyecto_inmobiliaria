// =========================================================
// BUSCADOR Y FILTROS DE PROPIEDADES
// =========================================================

document.getElementById('form-buscar').addEventListener('submit', async function (e) {
    e.preventDefault();

    const termino = document.getElementById('input-buscar').value.trim();
    const tipo = document.getElementById('filtro-tipo').value;
    const precioDesde = document.getElementById('precio-desde').value;
    const precioHasta = document.getElementById('precio-hasta').value;

    const parametros = new URLSearchParams();

    if (termino !== '') {
        parametros.append('buscar', termino);
    }

    if (tipo !== '') {
        parametros.append('tipo', tipo);
    }

    if (precioDesde !== '') {
        parametros.append('precio_desde', precioDesde);
    }

    if (precioHasta !== '') {
        parametros.append('precio_hasta', precioHasta);
    }

    try {

        const respuesta = await fetch(
            `/api/propiedades?${parametros.toString()}`
        );

        if (!respuesta.ok) {
            throw new Error('No se pudieron buscar las propiedades.');
        }

        const propiedades = await respuesta.json();

        mostrarResultados(propiedades);

    } catch (error) {

        console.error(error);

        alert('Ocurrió un error al realizar la búsqueda.');
    }
});


// =========================================================
// MOSTRAR RESULTADOS
// =========================================================

function mostrarResultados(propiedades) {

    const contenedor = document.querySelector('.prop-grid');

    if (!contenedor) {
        return;
    }

    contenedor.innerHTML = '';

    if (propiedades.length === 0) {

        contenedor.innerHTML = `
            <p class="sin-resultados">
                No encontramos propiedades que coincidan con tu búsqueda.
            </p>
        `;

        return;
    }

    propiedades.forEach(propiedad => {

        const tarjeta = document.createElement('a');

        tarjeta.href = `/propiedad/${propiedad.id}`;
        tarjeta.className = 'prop-card';

        tarjeta.innerHTML = `
            <div class="prop-img-container">

                <img
                    src="${propiedad.imagen_url || 'https://via.placeholder.com/300x200'}"
                    alt="${propiedad.tipo}"
                >

                <span class="prop-price">
                    $${Number(propiedad.precio).toLocaleString('es-AR')}
                </span>

            </div>

            <div class="prop-info">

                <h5>${propiedad.titulo}</h5>

                <p>
                    <i class="fa-solid fa-location-dot"></i>
                    ${propiedad.ubicacion}
                </p>

            </div>
        `;

        contenedor.appendChild(tarjeta);
    });
}