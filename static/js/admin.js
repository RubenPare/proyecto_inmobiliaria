// =========================================================
// PANEL ADMINISTRATIVO
// Gustavo Behrens Propiedades
// =========================================================


const formulario = document.getElementById("form-propiedad");

const tabla = document.getElementById("tabla-propiedades");

const mensaje = document.getElementById("mensaje");

const botonActualizar = document.getElementById("btn-actualizar");


// =========================================================
// MOSTRAR MENSAJE
// =========================================================

function mostrarMensaje(texto, tipo) {

    mensaje.textContent = texto;

    mensaje.className = "mensaje " + tipo;

}


// =========================================================
// CARGAR PROPIEDADES
// =========================================================

async function cargarPropiedades() {

    try {

        const respuesta = await fetch("/api/propiedades/admin");

        if (!respuesta.ok) {

            throw new Error(
                "No se pudieron cargar las propiedades."
            );

        }

        const propiedades = await respuesta.json();


        tabla.innerHTML = "";


        if (propiedades.length === 0) {

            tabla.innerHTML = `
                <tr>
                    <td colspan="6">
                        No hay propiedades cargadas.
                    </td>
                </tr>
            `;

            return;
        }


        propiedades.forEach(propiedad => {

            const fila = document.createElement("tr");


            fila.innerHTML = `
    <td>${propiedad.id}</td>

    <td>${propiedad.tipo}</td>

    <td>${propiedad.titulo}</td>

    <td>
        $${Number(propiedad.precio).toLocaleString("es-AR")}
    </td>

    <td>${propiedad.ubicacion}</td>

    <td>
        <span class="${propiedad.activo ? 'estado-activo' : 'estado-inactivo'}">
            ${propiedad.activo ? 'Activa' : 'Desactivada'}
        </span>
    </td>

    <td class="acciones">

        <a
            href="/propiedad/${propiedad.id}"
            target="_blank"
            class="btn-ver"
        >
            Ver
        </a>

        <button
            type="button"
            class="btn-editar"
            onclick="editarPropiedad(${propiedad.id})"
        >
            Editar
        </button>

        <button
            type="button"
            class="btn-estado"
            onclick="cambiarEstado(${propiedad.id})"
        >
            ${propiedad.activo ? 'Desactivar' : 'Activar'}
        </button>

        <button
            type="button"
            class="btn-eliminar"
            onclick="eliminarPropiedad(${propiedad.id})"
        >
            Eliminar
        </button>

    </td>
`;

            tabla.appendChild(fila);

        });

    }

    catch (error) {

        console.error(error);

        tabla.innerHTML = `

            <tr>

                <td colspan="6">

                    Error al cargar las propiedades.

                </td>

            </tr>

        `;

    }

}


// =========================================================
// GUARDAR PROPIEDAD
// =========================================================

formulario.addEventListener("submit", async function(event) {

    event.preventDefault();

    const propiedad = {
        tipo: document.getElementById("tipo").value,
        titulo: document.getElementById("titulo").value,
        descripcion: document.getElementById("descripcion").value,
        precio: Number(document.getElementById("precio").value),
        ubicacion: document.getElementById("ubicacion").value,
        imagen_url: document.getElementById("imagen_url").value
    };

    try {

        mostrarMensaje("Guardando propiedad...", "exito");

        let url = "/api/propiedades";
        let metodo = "POST";

        // Si estamos editando, usamos PUT
        if (formulario.dataset.editando) {

            url = `/api/propiedades/${formulario.dataset.editando}`;
            metodo = "PUT";
        }

        const respuesta = await fetch(
            url,
            {
                method: metodo,
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(propiedad)
            }
        );

        if (!respuesta.ok) {

            const error = await respuesta.text();

            console.error(error);

            throw new Error(
                "No se pudo guardar la propiedad."
            );
        }

        const propiedadGuardada = await respuesta.json();

        if (formulario.dataset.editando) {

            mostrarMensaje(
                `Propiedad "${propiedadGuardada.titulo}" actualizada correctamente.`,
                "exito"
            );

        } else {

            mostrarMensaje(
                `Propiedad "${propiedadGuardada.titulo}" guardada correctamente.`,
                "exito"
            );
        }

        formulario.reset();

        delete formulario.dataset.editando;

        document.querySelector(".btn-guardar").textContent =
            "Guardar propiedad";

        await cargarPropiedades();

    } catch (error) {

        console.error(error);

        mostrarMensaje(
            "Error al guardar la propiedad.",
            "error"
        );
    }
});

// =========================================================
// BOTÓN ACTUALIZAR
// =========================================================

botonActualizar.addEventListener(
    "click",
    cargarPropiedades
);


// =========================================================
// INICIO
// =========================================================

cargarPropiedades();
// =========================================================
// EDITAR PROPIEDAD
// =========================================================

async function editarPropiedad(id) {

    const respuesta = await fetch(`/api/propiedades/admin`);

    if (!respuesta.ok) {
        alert("No se pudieron cargar las propiedades.");
        return;
    }

    const propiedades = await respuesta.json();

    const propiedad = propiedades.find(p => p.id === id);

    if (!propiedad) {
        alert("Propiedad no encontrada.");
        return;
    }

    document.getElementById("tipo").value = propiedad.tipo;
    document.getElementById("titulo").value = propiedad.titulo;
    document.getElementById("precio").value = propiedad.precio;
    document.getElementById("ubicacion").value = propiedad.ubicacion;
    document.getElementById("imagen_url").value = propiedad.imagen_url || "";
    document.getElementById("descripcion").value = propiedad.descripcion || "";

    formulario.dataset.editando = id;

    document.querySelector(".btn-guardar").textContent =
        "Actualizar propiedad";

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


// =========================================================
// CAMBIAR ESTADO
// =========================================================

async function cambiarEstado(id) {

    const confirmar = confirm(
        "¿Querés cambiar el estado de esta propiedad?"
    );

    if (!confirmar) {
        return;
    }

    const respuesta = await fetch(
        `/api/propiedades/${id}/estado`,
        {
            method: "PUT"
        }
    );

    if (!respuesta.ok) {
        alert("No se pudo cambiar el estado.");
        return;
    }

    await cargarPropiedades();
}


// =========================================================
// ELIMINAR
// =========================================================

async function eliminarPropiedad(id) {

    const confirmar = confirm(
        "¿Estás seguro de eliminar definitivamente esta propiedad?"
    );

    if (!confirmar) {
        return;
    }

    const respuesta = await fetch(
        `/api/propiedades/${id}`,
        {
            method: "DELETE"
        }
    );

    if (!respuesta.ok) {
        alert("No se pudo eliminar la propiedad.");
        return;
    }

    await cargarPropiedades();
}