from models import db
from models.editorial import Editorial
from models.libro import Libro
from services.prestamo_service import obtener_estado_libro
from utils.errors import ApiError
from utils.validators import (
    sanitize_string,
    validate_allowed_fields,
    validate_isbn,
    validate_positive_int,
)

ALLOWED_FIELDS = {
    "titulo",
    "autor",
    "editorial_id",
    "isbn",
    "categoria",
    "ubicacion",
    "activo",
}


def list_libros():
    return Libro.query.order_by(Libro.titulo.asc()).all()


def _validate_editorial(editorial_id):
    if editorial_id is None:
        return
    validate_positive_int(editorial_id, "editorial_id")
    editorial = Editorial.query.get(editorial_id)
    if not editorial:
        raise ApiError("editorial_id inválido", 400)


def create_libro(payload: dict) -> Libro:
    validate_allowed_fields(payload, ALLOWED_FIELDS)

    titulo = sanitize_string(payload.get("titulo"), "titulo", 255, required=True)
    autor = sanitize_string(payload.get("autor"), "autor", 255, required=True)

    editorial_id = payload.get("editorial_id")
    _validate_editorial(editorial_id)

    isbn_raw = sanitize_string(payload.get("isbn"), "isbn", 32)

    libro = Libro(
        titulo=titulo,
        autor=autor,
        editorial_id=editorial_id,
        isbn=validate_isbn(isbn_raw),
        categoria=sanitize_string(payload.get("categoria"), "categoria", 120),
        ubicacion=sanitize_string(payload.get("ubicacion"), "ubicacion", 120),
    )
    db.session.add(libro)
    db.session.commit()
    return libro


def update_libro(libro_id: int, payload: dict) -> Libro:
    libro = Libro.query.get(libro_id)
    if not libro:
        raise ApiError("Libro no encontrado", 404)

    validate_allowed_fields(payload, ALLOWED_FIELDS)

    if "titulo" in payload:
        libro.titulo = sanitize_string(payload.get("titulo"), "titulo", 255, required=True)

    if "autor" in payload:
        libro.autor = sanitize_string(payload.get("autor"), "autor", 255, required=True)

    if "editorial_id" in payload:
        _validate_editorial(payload.get("editorial_id"))
        libro.editorial_id = payload.get("editorial_id")

    if "isbn" in payload:
        isbn_raw = sanitize_string(payload.get("isbn"), "isbn", 32)
        libro.isbn = validate_isbn(isbn_raw)

    if "categoria" in payload:
        libro.categoria = sanitize_string(payload.get("categoria"), "categoria", 120)

    if "ubicacion" in payload:
        libro.ubicacion = sanitize_string(payload.get("ubicacion"), "ubicacion", 120)

    if "activo" in payload:
        if not isinstance(payload.get("activo"), bool):
            raise ApiError("activo debe ser boolean", 400)
        libro.activo = payload.get("activo")

    db.session.commit()
    return libro


def soft_delete_libro(libro_id: int) -> Libro:
    libro = Libro.query.get(libro_id)
    if not libro:
        raise ApiError("Libro no encontrado", 404)
    libro.activo = False
    db.session.commit()
    return libro


def libro_with_status(libro: Libro) -> dict:
    base = libro.to_dict()
    if libro.activo:
        estado_data = obtener_estado_libro(libro.id)
    else:
        estado_data = {"estado": "INACTIVO", "vencido": False, "prestamo_id": None}

    return {**base, **estado_data}
