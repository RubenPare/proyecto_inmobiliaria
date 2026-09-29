from fastapi import FastAPI, Request, Depends, Form
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

from database import Base, engine, get_db
from models import Propiedad
class PropiedadCreate(BaseModel):
    tipo: str
    titulo: str
    descripcion: str | None = None
    precio: float
    ubicacion: str
    imagen_url: str | None = None

# ============================================================

# APLICACIÓN

# ============================================================

app = FastAPI(title="Gustavo Behrens Propiedades")
app.add_middleware(
    SessionMiddleware,
    secret_key="gustavo-behrens-clave-temporal"
)
# ============================================================

# CREAR TABLAS

# ============================================================

Base.metadata.create_all(bind=engine)

# ============================================================

# ARCHIVOS ESTÁTICOS

# ============================================================

app.mount("/static", StaticFiles(directory="static"), name="static")

# ============================================================

# PLANTILLAS

# ============================================================

templates = Jinja2Templates(directory="templates")

# ============================================================

# PÁGINA PRINCIPAL

# ============================================================

@app.get("/")
def home(
    request: Request,
    db: Session = Depends(get_db)
):
    """Página principal."""

    propiedades = db.query(Propiedad).filter(Propiedad.activo == 1).all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "propiedades": propiedades
        }
    )
# ============================================================

# DETALLE DE PROPIEDAD

# ============================================================

@app.get("/propiedad/{propiedad_id}")
def detalle_propiedad(
    request: Request,
    propiedad_id: int,
    db: Session = Depends(get_db)
):
    propiedad = db.query(Propiedad).filter(
        Propiedad.id == propiedad_id
    ).first()

    print("PROPIEDAD ENCONTRADA:", propiedad)
    print("ARCHIVO HTML USADO:", templates.get_template("propiedad.html").filename)

    return templates.TemplateResponse(
        request=request,
        name="propiedad.html",
        context={
            "propiedad": propiedad
        }
    )
# ============================================================

# ADMINISTRACIÓN

# ============================================================
# =========================================================
# LOGIN ADMINISTRATIVO
# =========================================================

ADMIN_USUARIO = "admin"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
@app.get("/prueba-admin")
def prueba_admin():
    return {
        "usuario_configurado": ADMIN_USUARIO,
        "password_configurada": bool(ADMIN_PASSWORD),
        "longitud_password": len(ADMIN_PASSWORD) if ADMIN_PASSWORD else 0
    }


def verificar_admin(request: Request):
    if not request.session.get("admin"):
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )

    return None


@app.get("/admin/login")
def admin_login(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="admin/login.html",
        context={"request": request}
    )

@app.post("/admin/login")
def admin_login_post(
    request: Request,
    usuario: str = Form(...),
    password: str = Form(...)
):
    print("USUARIO RECIBIDO:", usuario)
    print("LONGITUD PASSWORD RECIBIDA:", len(password))

    if usuario == ADMIN_USUARIO and password == ADMIN_PASSWORD:
        request.session["admin"] = True

        return RedirectResponse(
            url="/admin/propiedades",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="admin/login.html",
        context={
            "request": request,
            "error": "Usuario o contraseña incorrectos."
        }
    )

@app.get("/admin/logout")
def admin_logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/admin/login",
        status_code=303
    )
@app.get("/admin/propiedades")
def admin_propiedades(request: Request):

    if not request.session.get("admin"):
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="admin/propiedades.html",
        context={"request": request}
    )
# ============================================================

# PRUEBA DE BASE DE DATOS

# ============================================================

@app.get("/api/estado-db")
def estado_db(db: Session = Depends(get_db)):
    """Comprueba que la tabla propiedades exista y sea accesible."""


    cantidad = db.query(Propiedad).count()
    return {
    "base_de_datos": "conectada",
    "tabla": "propiedades",
    "cantidad_propiedades": cantidad
}
# ============================================================
# API DE PROPIEDADES
# ============================================================

@app.get("/api/propiedades")
def listar_propiedades(
    buscar: str = "",
    tipo: str = "",
    precio_desde: float | None = None,
    precio_hasta: float | None = None,
    db: Session = Depends(get_db)
):
    """Lista propiedades activas con filtros."""

    consulta = db.query(Propiedad).filter(
        Propiedad.activo == 1
    )

    # Búsqueda por texto
    if buscar.strip():
        termino = f"%{buscar.strip()}%"

        consulta = consulta.filter(
            (Propiedad.titulo.ilike(termino)) |
            (Propiedad.tipo.ilike(termino)) |
            (Propiedad.ubicacion.ilike(termino)) |
            (Propiedad.descripcion.ilike(termino))
        )

    # Filtro por tipo
    if tipo.strip():
        consulta = consulta.filter(
            Propiedad.tipo.ilike(tipo.strip())
        )

    # Filtro por precio mínimo
    if precio_desde is not None:
        consulta = consulta.filter(
            Propiedad.precio >= precio_desde
        )

    # Filtro por precio máximo
    if precio_hasta is not None:
        consulta = consulta.filter(
            Propiedad.precio <= precio_hasta
        )

    return consulta.all()

@app.get("/api/propiedades/admin")
def listar_propiedades_admin(db: Session = Depends(get_db)):
    """Lista todas las propiedades para administración."""

    propiedades = db.query(Propiedad).all()

    return propiedades

@app.post("/api/propiedades")
def crear_propiedad(
    request: Request,
    propiedad: PropiedadCreate,
    db: Session = Depends(get_db)
):
    acceso = verificar_admin(request)

    if acceso:
        return acceso

    """Crea una nueva propiedad."""

    nueva_propiedad = Propiedad(
        tipo=propiedad.tipo,
        titulo=propiedad.titulo,
        descripcion=propiedad.descripcion,
        precio=propiedad.precio,
        ubicacion=propiedad.ubicacion,
        imagen_url=propiedad.imagen_url
    )

    db.add(nueva_propiedad)
    db.commit()
    db.refresh(nueva_propiedad)

    return nueva_propiedad
# =========================================================
# EDITAR PROPIEDAD
# =========================================================
@app.put("/api/propiedades/{propiedad_id}")
def editar_propiedad(
    request: Request,
    propiedad_id: int,
    propiedad: PropiedadCreate,
    db: Session = Depends(get_db)
):
    acceso = verificar_admin(request)

    if acceso:
        return acceso

    existente = db.query(Propiedad).filter(
        Propiedad.id == propiedad_id
    ).first()

    if not existente:
        return {"error": "Propiedad no encontrada"}

    existente.tipo = propiedad.tipo
@app.put("/api/propiedades/{propiedad_id}/estado")
def cambiar_estado_propiedad(
    request: Request,
    propiedad_id: int,
    db: Session = Depends(get_db)
):
    acceso = verificar_admin(request)

    if acceso:
        return acceso

    propiedad = db.query(Propiedad).filter(
        Propiedad.id == propiedad_id
    ).first()

    if not propiedad:
        return {"error": "Propiedad no encontrada"}

    propiedad.activo = not propiedad.activo

    db.commit()
    db.refresh(propiedad)

    return propiedad


# =========================================================
# DESACTIVAR / ACTIVAR PROPIEDAD
# =========================================================

@app.put("/api/propiedades/{propiedad_id}/estado")
def cambiar_estado_propiedad(
    propiedad_id: int,
    db: Session = Depends(get_db)
):
    propiedad = db.query(Propiedad).filter(
        Propiedad.id == propiedad_id
    ).first()

    if not propiedad:
        return {"error": "Propiedad no encontrada"}

    propiedad.activo = not propiedad.activo

    db.commit()
    db.refresh(propiedad)

    return propiedad


# =========================================================
# ELIMINAR PROPIEDAD DEFINITIVAMENTE
# =========================================================

@app.delete("/api/propiedades/{propiedad_id}")
def eliminar_propiedad(
    request: Request,
    propiedad_id: int,
    db: Session = Depends(get_db)
):
    acceso = verificar_admin(request)

    if acceso:
        return acceso

    propiedad = db.query(Propiedad).filter(
        Propiedad.id == propiedad_id
    ).first()

    if not propiedad:
        return {"error": "Propiedad no encontrada"}

    db.delete(propiedad)
    db.commit()

    return {
        "mensaje": "Propiedad eliminada correctamente",
        "id": propiedad_id
    }

# ============================================================

# DESARROLLO

# ============================================================

# Ejecutar con:

# uvicorn main:app --reload
