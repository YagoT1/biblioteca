import logging

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from models import db
from models.libro import Libro
from models.prestamo import Prestamo
from utils.datetime import ensure_utc, utc_now
from utils.errors import ApiError
from utils.validators import validate_future_due_date

logger = logging.getLogger(__name__)


def _get_libro_or_404(libro_id: int) -> Libro:
    libro = Libro.query.get(libro_id)
    if not libro or not libro.activo:
        raise ApiError("Libro no encontrado", 404)
    return libro


def verificar_libro_disponible(libro_id: int) -> bool:
    _get_libro_or_404(libro_id)
    prestamo_activo = Prestamo.query.filter(
        and_(Prestamo.libro_id == libro_id, Prestamo.fecha_devolucion.is_(None))
    ).first()
    return prestamo_activo is None


def obtener_estado_libro(libro_id: int) -> dict:
    _get_libro_or_404(libro_id)

    prestamo_activo = Prestamo.query.filter(
        and_(Prestamo.libro_id == libro_id, Prestamo.fecha_devolucion.is_(None))
    ).first()

    if not prestamo_activo:
        return {"estado": "DISPONIBLE", "vencido": False, "prestamo_id": None}

    vencido = ensure_utc(prestamo_activo.fecha_vencimiento) < utc_now()
    return {
        "estado": "PRESTADO",
        "vencido": vencido,
        "prestamo_id": prestamo_activo.id,
    }


def crear_prestamo(libro_id: int, fecha_vencimiento) -> Prestamo:
    fecha_salida = utc_now()
    fecha_vencimiento_utc = validate_future_due_date(fecha_vencimiento, fecha_salida)

    try:
        with db.session.begin():
            # Lock pesimista para serializar préstamos del mismo libro.
            libro = (
                db.session.query(Libro)
                .filter(Libro.id == libro_id, Libro.activo.is_(True))
                .with_for_update()
                .first()
            )
            if not libro:
                raise ApiError("Libro no encontrado", 404)

            prestamo_activo = (
                db.session.query(Prestamo)
                .filter(
                    Prestamo.libro_id == libro_id,
                    Prestamo.fecha_devolucion.is_(None),
                )
                .with_for_update()
                .first()
            )

            if prestamo_activo:
                raise ApiError("El libro ya tiene un préstamo activo", 409)

            prestamo = Prestamo(
                libro_id=libro_id,
                fecha_salida=fecha_salida,
                fecha_vencimiento=fecha_vencimiento_utc,
            )
            db.session.add(prestamo)
            db.session.flush()

        logger.info("prestamo_creado libro_id=%s prestamo_id=%s", libro_id, prestamo.id)
        return prestamo
    except IntegrityError as exc:
        db.session.rollback()
        logger.warning("conflicto_concurrencia_prestamo libro_id=%s", libro_id)
        raise ApiError("El libro ya tiene un préstamo activo", 409) from exc


def devolver_libro(prestamo_id: int) -> Prestamo:
    prestamo = Prestamo.query.get(prestamo_id)
    if not prestamo:
        raise ApiError("Préstamo no encontrado", 404)

    if prestamo.fecha_devolucion is not None:
        raise ApiError("El préstamo ya fue devuelto", 409)

    prestamo.fecha_devolucion = utc_now()
    db.session.commit()
    logger.info("prestamo_devuelto prestamo_id=%s libro_id=%s", prestamo.id, prestamo.libro_id)
    return prestamo
