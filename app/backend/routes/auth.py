from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from services.auth_service import verificar_usuario
from utils.errors import ApiError
from utils.responses import api_response
from utils.validators import require_json_object

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True)
    require_json_object(payload)

    username = payload.get("username")
    password = payload.get("password")
    user = verificar_usuario(username, password)
    if not user:
        raise ApiError("Credenciales inválidas", 401)

    token = create_access_token(identity=str(user.id), additional_claims={"username": user.username})
    return api_response(True, {"token": token}, None, 200)
