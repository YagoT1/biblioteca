from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from models.editorial import Editorial  # noqa: E402,F401
from models.libro import Libro  # noqa: E402,F401
from models.prestamo import Prestamo  # noqa: E402,F401

from models.usuario import Usuario  # noqa: E402,F401
