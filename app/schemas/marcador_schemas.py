from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID

from app.domain.enums import Estatus

class MarcadorSchemaCreate(BaseModel):
    usuario_id: UUID
    libro_id: UUID
    pagina: int
    capitulo: int
    cita: Optional[str] = None
    nota: Optional[str] = None
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)

class MarcadorSchemaResponse(BaseModel):
    id: UUID
    usuario_id: UUID
    libro_id: UUID
    capitulo: int
    pagina: int
    cita: Optional[str] = None
    nota: Optional[str] = None
    fecha_creacion: datetime

class MarcadorSchemaUpdate(BaseModel):
    capitulo: Optional[int] = None
    pagina: Optional[int] = None
    cita: Optional[str] = None
    nota: Optional[str] = None
    fecha_creacion: Optional[datetime] = None