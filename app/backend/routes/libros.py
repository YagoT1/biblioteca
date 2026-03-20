from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from services.libro_service import (
    create_libro,
    libro_with_status,
    list_libros,
    soft_delete_libro,
    update_libro,
)
from utils.responses import api_response
from utils.validators import require_json_object

libros_bp = Blueprint("libros", __name__)


@libros_bp.get("")
@jwt_required()
def get_libros():
    libros = [libro_with_status(libro) for libro in list_libros()]
    return api_response(True, libros, None, 200)


@libros_bp.post("")
@jwt_required()
def post_libro():
    payload = request.get_json(silent=True)
    require_json_object(payload)

    libro = create_libro(payload)
    return api_response(True, libro_with_status(libro), None, 201)


@libros_bp.put("/<int:libro_id>")
@jwt_required()
def put_libro(libro_id: int):
    payload = request.get_json(silent=True)
    require_json_object(payload)

    libro = update_libro(libro_id, payload)
    return api_response(True, libro_with_status(libro), None, 200)


@libros_bp.delete("/<int:libro_id>")
@jwt_required()
def delete_libro(libro_id: int):
    libro = soft_delete_libro(libro_id)
    return api_response(True, libro_with_status(libro), None, 200)
