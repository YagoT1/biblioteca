import logging

from flask import Flask
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from utils.responses import api_response

logger = logging.getLogger(__name__)


class ApiError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def register_error_handlers(app: Flask):
    @app.errorhandler(ApiError)
    def handle_api_error(error: ApiError):
        return api_response(False, {}, error.message, error.status_code)

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(_error: IntegrityError):
        logger.warning("IntegrityError", exc_info=app.config.get("DEBUG", False))
        return api_response(False, {}, "Violación de integridad de datos", 409)

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        return api_response(False, {}, error.description, error.code or 400)

    @app.errorhandler(Exception)
    def handle_generic_error(_error: Exception):
        logger.error("Error no controlado", exc_info=app.config.get("DEBUG", False))
        if app.config.get("DEBUG"):
            return api_response(False, {}, str(_error), 500)
        return api_response(False, {}, "Error interno del servidor", 500)


def register_jwt_error_handlers(jwt: JWTManager):
    @jwt.unauthorized_loader
    def unauthorized_callback(_msg):
        return api_response(False, {}, "Se requiere token de acceso", 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(_msg):
        return api_response(False, {}, "Token inválido", 401)

    @jwt.expired_token_loader
    def expired_token_callback(_jwt_header, _jwt_payload):
        return api_response(False, {}, "Token expirado", 401)
