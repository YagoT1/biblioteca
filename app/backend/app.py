import logging
from logging.config import dictConfig

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import get_config
from models import db
from routes.auth import auth_bp
from routes.editoriales import editoriales_bp
from routes.libros import libros_bp
from routes.prestamos import prestamos_bp
from utils.errors import register_error_handlers, register_jwt_error_handlers


def configure_logging(app: Flask):
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
                }
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "level": "INFO",
                }
            },
            "root": {"handlers": ["default"], "level": "INFO"},
        }
    )
    app.logger.setLevel(logging.INFO)


def create_app(config_name: str | None = None) -> Flask:
    """Application Factory principal."""
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("DATABASE_URL no configurada")
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY no configurada")
    if not app.config.get("JWT_SECRET_KEY"):
        raise RuntimeError("JWT_SECRET_KEY no configurada")

    configure_logging(app)

    CORS(app)
    db.init_app(app)

    jwt = JWTManager(app)

    # Blueprints API
    app.register_blueprint(auth_bp)
    app.register_blueprint(editoriales_bp, url_prefix="/editoriales")
    app.register_blueprint(libros_bp, url_prefix="/libros")
    app.register_blueprint(prestamos_bp, url_prefix="/prestamos")

    # Manejador centralizado de errores
    register_error_handlers(app)
    register_jwt_error_handlers(jwt)

    @app.get("/health")
    def health_check():
        return {"status": "ok"}, 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
