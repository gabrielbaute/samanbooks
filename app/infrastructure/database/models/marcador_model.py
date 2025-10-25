from app.infrastructure.database.db_config import db
from app.infrastructure.database.extensions import GUID
from datetime import datetime
import uuid

class MarcadorModel(db.Model):
    __tablename__ = "marcadores"

    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    usuario_id = db.Column(GUID(), db.ForeignKey("usuarios.id"), nullable=False)
    libro_id = db.Column(GUID(), db.ForeignKey("libros.id"), nullable=False)
    pagina = db.Column(db.Integer, nullable=False)
    cita = db.Column(db.Text, nullable=False)
    nota = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)