from models import db
from utils.datetime import utc_now


class Editorial(db.Model):
    __tablename__ = "editoriales"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    pais = db.Column(db.String(120), nullable=True)
    estado = db.Column(db.String(20), nullable=False, default="activo")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    libros = db.relationship("Libro", back_populates="editorial", lazy="select")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "pais": self.pais,
            "estado": self.estado,
        }
