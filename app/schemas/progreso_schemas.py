from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID

from app.domain.enums import Estatus

class ProgresoSchemaCreate(BaseModel):
    usuario_id: UUID
    libro_id: UUID
    porcentaje: float
    estatus: Estatus = Estatus.PENDIENTE
    ultima_fecha: datetime = Field(default_factory=datetime.utcnow)

class ProgresoSchemaResponse(BaseModel):
    usuario_id: UUID
    libro_id: UUID
    porcentaje: float
    estatus: Estatus
    ultima_fecha: datetime

class ProgresoSchemaUpdate(BaseModel):
    usuario_id: UUID
    libro_id: UUID
    porcentaje: float
    estatus: Estatus
    ultima_fecha: datetime = Field(default_factory=datetime.utcnow)