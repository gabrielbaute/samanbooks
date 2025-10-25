import uuid
from app.infrastructure.database.db_config import db

class SerieModel(db.Model):
    __tablename__ = "series"

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    autor_id = db.Column(db.Uuid, db.ForeignKey("autores.id"), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    portada_hash = db.Column(db.String(255))
    

    libros = db.relationship("LibroModel", back_populates="serie")
    autor = db.relationship("AutorModel", back_populates="series")