import uuid
from datetime import datetime
from sqlalchemy import Enum

from app.infrastructure.database.db_config import db
from app.infrastructure.database.extensions import GUID
from app.domain.enums import Estatus

class ProgresoModel(db.Model):
    __tablename__ = "progresos"

    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    usuario_id = db.Column(GUID(), db.ForeignKey("usuarios.id"), nullable=False)
    libro_id = db.Column(GUID(), db.ForeignKey("libros.id"), nullable=False)
    porcentaje = db.Column(db.Float, nullable=False)
    estatus = db.Column(Enum(Estatus, name="estatus_enum"), nullable=False, default=Estatus.PENDIENTE)
    ultima_fecha = db.Column(db.DateTime, default=datetime.utcnow)
