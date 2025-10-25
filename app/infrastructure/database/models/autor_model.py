import uuid

from app.infrastructure.database.db_config import db
from app.infrastructure.database.extensions import GUID

class AutorModel(db.Model):
    __tablename__ = "autores"

    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    nombre = db.Column(db.String(255), nullable=False)
    foto_hash = db.Column(db.String(255), nullable=True)
    biografia = db.Column(db.Text)
    fecha_nacimiento = db.Column(db.Date)
    fecha_muerte = db.Column(db.Date)
    nacionalidad = db.Column(db.String(255))
    redes_sociales = db.Column(db.JSON)

    libros = db.relationship(
        "LibroModel",
        secondary="libros_autores",
        back_populates="autores"
    )
