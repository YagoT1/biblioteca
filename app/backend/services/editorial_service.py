from models import db
from models.editorial import Editorial
from utils.errors import ApiError
from utils.validators import sanitize_string, validate_allowed_fields

ALLOWED_FIELDS = {"nombre", "pais", "estado"}


def list_editoriales():
    return Editorial.query.order_by(Editorial.nombre.asc()).all()


def create_editorial(payload: dict) -> Editorial:
    validate_allowed_fields(payload, ALLOWED_FIELDS)

    nombre = sanitize_string(payload.get("nombre"), "nombre", 255, required=True)
    pais = sanitize_string(payload.get("pais"), "pais", 120)
    estado = sanitize_string(payload.get("estado"), "estado", 20) or "activo"

    if estado not in {"activo", "inactivo"}:
        raise ApiError("estado debe ser activo o inactivo", 400)

    editorial = Editorial(nombre=nombre, pais=pais, estado=estado)
    db.session.add(editorial)
    db.session.commit()
    return editorial


def update_editorial(editorial_id: int, payload: dict) -> Editorial:
    editorial = Editorial.query.get(editorial_id)
    if not editorial:
        raise ApiError("Editorial no encontrada", 404)

    validate_allowed_fields(payload, ALLOWED_FIELDS)

    if "nombre" in payload:
        editorial.nombre = sanitize_string(payload.get("nombre"), "nombre", 255, required=True)

    if "pais" in payload:
        editorial.pais = sanitize_string(payload.get("pais"), "pais", 120)

    if "estado" in payload:
        estado = sanitize_string(payload.get("estado"), "estado", 20, required=True)
        if estado not in {"activo", "inactivo"}:
            raise ApiError("estado debe ser activo o inactivo", 400)
        editorial.estado = estado

    db.session.commit()
    return editorial


def delete_editorial(editorial_id: int):
    editorial = Editorial.query.get(editorial_id)
    if not editorial:
        raise ApiError("Editorial no encontrada", 404)

    editorial.estado = "inactivo"
    db.session.commit()
