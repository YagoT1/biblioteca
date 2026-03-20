from flask import Blueprint, request

from services.editorial_service import (
    create_editorial,
    delete_editorial,
    list_editoriales,
    update_editorial,
)
from utils.responses import api_response
from utils.validators import require_json_object

editoriales_bp = Blueprint("editoriales", __name__)


@editoriales_bp.get("")
def get_editoriales():
    editoriales = [e.to_dict() for e in list_editoriales()]
    return api_response(True, editoriales, None, 200)


@editoriales_bp.post("")
def post_editorial():
    payload = request.get_json(silent=True)
    require_json_object(payload)

    editorial = create_editorial(payload)
    return api_response(True, editorial.to_dict(), None, 201)


@editoriales_bp.put("/<int:editorial_id>")
def put_editorial(editorial_id: int):
    payload = request.get_json(silent=True)
    require_json_object(payload)

    editorial = update_editorial(editorial_id, payload)
    return api_response(True, editorial.to_dict(), None, 200)


@editoriales_bp.delete("/<int:editorial_id>")
def remove_editorial(editorial_id: int):
    delete_editorial(editorial_id)
    return api_response(True, {"message": "Editorial inactivada"}, None, 200)
