from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from app.domain.enums import Estatus

class Progreso(BaseModel):
    usuario_id: UUID
    libro_id: UUID
    porcentaje: float
    estatus: Estatus = Estatus.PENDIENTE
    ultima_fecha: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("porcentaje")
    @classmethod
    def validar_porcentaje(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        return v