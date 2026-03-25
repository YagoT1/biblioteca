"""Script para crear usuario administrador inicial.

⚠️ Cambiar la contraseña inicial en producción inmediatamente.
Credenciales iniciales por defecto:
- username: admin
- password: admin123
"""

from app import create_app
from models.usuario import Usuario
from services.auth_service import crear_usuario
from utils.errors import ApiError

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"


def main():
    app = create_app()
    with app.app_context():
        existing = Usuario.query.filter_by(username=DEFAULT_ADMIN_USERNAME).first()
        if existing:
            print("El usuario admin ya existe. No se creó duplicado.")
            return

        try:
            user = crear_usuario(DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD)
            print(f"Usuario admin creado: {user.username}")
            print("IMPORTANTE: Cambiar la contraseña 'admin123' en producción.")
        except ApiError as exc:
            print(f"Error al crear admin: {exc.message}")


if __name__ == "__main__":
    main()
