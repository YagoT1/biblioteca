import getpass
import os

from app import create_app
from services.auth_service import crear_usuario
from utils.errors import ApiError


def main():
    username = os.getenv("ADMIN_USERNAME") or input("Username admin: ").strip()
    password = os.getenv("ADMIN_PASSWORD") or getpass.getpass("Password admin: ")

    app = create_app()
    with app.app_context():
        try:
            user = crear_usuario(username, password)
            print(f"Usuario admin creado: {user.username}")
        except ApiError as exc:
            print(f"Error: {exc.message}")


if __name__ == "__main__":
    main()
