from models import db
from utils.datetime import utc_now


class Prestamo(db.Model):
    __tablename__ = "prestamos"
    __table_args__ = (
        db.Index(
            "uq_prestamo_activo_por_libro",
            "libro_id",
            unique=True,
            postgresql_where=db.text("fecha_devolucion IS NULL"),
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(db.Integer, db.ForeignKey("libros.id"), nullable=False, index=True)
    fecha_salida = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    fecha_vencimiento = db.Column(db.DateTime(timezone=True), nullable=False)
    fecha_devolucion = db.Column(db.DateTime(timezone=True), nullable=True)

    libro = db.relationship("Libro", back_populates="prestamos")

    def to_dict(self):
        return {
            "id": self.id,
            "libro_id": self.libro_id,
            "fecha_salida": self.fecha_salida.isoformat(),
            "fecha_vencimiento": self.fecha_vencimiento.isoformat(),
            "fecha_devolucion": self.fecha_devolucion.isoformat() if self.fecha_devolucion else None,
        }
