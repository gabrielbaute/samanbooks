from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID, uuid4
from datetime import date

from app.domain.enums import Rol

class Usuario(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    username: str
    password_hash: str
    email: EmailStr
    rol: Rol = Rol.LECTOR
    fecha_registro: date = Field(default_factory=date.today)