from datetime import date
from sqlalchemy import Enum
import uuid

from app.domain.enums import Rol
from app.infrastructure.database.db_config import db
from app.infrastructure.database.extensions import GUID


class UsuarioModel(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    rol = db.Column(Enum(Rol, name="rol_enum"), nullable=False, default=Rol.LECTOR)
    fecha_registro = db.Column(db.Date, default=date.today)
