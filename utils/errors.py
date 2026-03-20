import logging

from flask import Flask
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
    def handle_integrity_error(error: IntegrityError):
        logger.warning("IntegrityError", exc_info=app.config.get("DEBUG", False))
        return api_response(False, {}, "Violación de integridad de datos", 409)

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        return api_response(False, {}, error.description, error.code or 400)

    @app.errorhandler(Exception)
    def handle_generic_error(error: Exception):
        logger.error("Error no controlado", exc_info=app.config.get("DEBUG", False))
        if app.config.get("DEBUG"):
            return api_response(False, {}, str(error), 500)
        return api_response(False, {}, "Error interno del servidor", 500)
