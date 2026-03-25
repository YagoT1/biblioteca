import bcrypt

from models import db
from models.usuario import Usuario
from utils.errors import ApiError
from utils.validators import sanitize_string


def _sanitize_username(username):
    return sanitize_string(username, "username", 120, required=True)


def crear_usuario(username: str, password: str) -> Usuario:
    normalized_username = _sanitize_username(username)
    normalized_password = sanitize_string(password, "password", 255, required=True)

    existing = Usuario.query.filter_by(username=normalized_username).first()
    if existing:
        raise ApiError("username ya existe", 409)

    hashed = bcrypt.hashpw(normalized_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user = Usuario(username=normalized_username, password_hash=hashed)
    db.session.add(user)
    db.session.commit()
    return user


def verificar_usuario(username: str, password: str):
    normalized_username = _sanitize_username(username)
    normalized_password = sanitize_string(password, "password", 255, required=True)

    user = Usuario.query.filter_by(username=normalized_username, is_active=True).first()
    if not user:
        return None

    valid = bcrypt.checkpw(normalized_password.encode("utf-8"), user.password_hash.encode("utf-8"))
    return user if valid else None
