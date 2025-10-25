from datetime import datetime
from sqlalchemy import Enum
import uuid

from app.infrastructure.database.db_config import db
from app.infrastructure.database.extensions import GUID
from app.domain.enums import Formato

class LibroModel(db.Model):
    __tablename__ = "libros"

    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    titulo = db.Column(db.String(255), nullable=False)
    path = db.Column(db.Text, nullable=False)
    formato = db.Column(Enum(Formato, name="formato_enum"), nullable=False)
    portada_hash = db.Column(db.String(64), nullable=False)
    isbn = db.Column(db.String(13))
    fecha_publicacion = db.Column(db.Date)
    editorial = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    paginas = db.Column(db.Integer)
    year = db.Column(db.Integer)

    serie_id = db.Column(db.Uuid, db.ForeignKey("series.id"), nullable=True)
    serie = db.relationship("SerieModel", back_populates="libros")

    autores = db.relationship(
        "AutorModel",
        secondary="libros_autores",
        back_populates="libros"
    )

# Tabla intermedia para relación N:M entre libros y autores
libros_autores = db.Table(
    "libros_autores",
    db.Column("libro_id", db.Uuid, db.ForeignKey("libros.id"), primary_key=True),
    db.Column("autor_id", db.Uuid, db.ForeignKey("autores.id"), primary_key=True)
)
