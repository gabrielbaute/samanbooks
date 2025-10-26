from flask_login import UserMixin
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date
from uuid import UUID

from app.domain.enums import Rol

class UsuarioSchemaCreate(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    rol: Rol = Rol.LECTOR
    fecha_registro: date = Field(default_factory=date.today)

class UsuarioSchemaResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    rol: Rol = Rol.LECTOR
    fecha_registro: date

class UsuarioSchemaLogin(BaseModel, UserMixin):
    email = EmailStr
    password: str

class UsuarioSchemaUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    rol: Optional[Rol] = None
    hashed_password: Optional[str] = None