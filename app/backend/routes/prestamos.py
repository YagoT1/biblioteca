from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import and_

from models.prestamo import Prestamo
from services.prestamo_service import crear_prestamo, devolver_libro
from utils.datetime import utc_now
from utils.responses import api_response
from utils.validators import parse_datetime, require_json_object, validate_positive_int

prestamos_bp = Blueprint("prestamos", __name__)


@prestamos_bp.post("")
@jwt_required()
def post_prestamo():
    payload = request.get_json(silent=True)
    require_json_object(payload)

    libro_id = validate_positive_int(payload.get("libro_id"), "libro_id")
    fecha_vencimiento = parse_datetime(payload.get("fecha_vencimiento"), "fecha_vencimiento")

    prestamo = crear_prestamo(libro_id, fecha_vencimiento)
    return api_response(True, prestamo.to_dict(), None, 201)


@prestamos_bp.post("/<int:prestamo_id>/devolver")
@jwt_required()
def post_devolver(prestamo_id: int):
    prestamo = devolver_libro(prestamo_id)
    return api_response(True, prestamo.to_dict(), None, 200)


@prestamos_bp.get("/activos")
@jwt_required()
def get_activos():
    activos = Prestamo.query.filter(Prestamo.fecha_devolucion.is_(None)).all()
    return api_response(True, [p.to_dict() for p in activos], None, 200)


@prestamos_bp.get("/vencidos")
@jwt_required()
def get_vencidos():
    now = utc_now()
    vencidos = Prestamo.query.filter(
        and_(Prestamo.fecha_vencimiento < now, Prestamo.fecha_devolucion.is_(None))
    ).all()
    return api_response(True, [p.to_dict() for p in vencidos], None, 200)
