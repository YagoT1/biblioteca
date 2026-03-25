from models import db
from utils.datetime import utc_now


class Libro(db.Model):
    __tablename__ = "libros"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255), nullable=False)
    editorial_id = db.Column(db.Integer, db.ForeignKey("editoriales.id"), nullable=True)
    isbn = db.Column(db.String(32), nullable=True, index=True)
    categoria = db.Column(db.String(120), nullable=True)
    ubicacion = db.Column(db.String(120), nullable=True)
    fecha_alta = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    editorial = db.relationship("Editorial", back_populates="libros")
    prestamos = db.relationship("Prestamo", back_populates="libro", lazy="select")

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "editorial_id": self.editorial_id,
            "isbn": self.isbn,
            "categoria": self.categoria,
            "ubicacion": self.ubicacion,
            "fecha_alta": self.fecha_alta.isoformat(),
            "activo": self.activo,
        }
