from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

class Marcador(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    usuario_id: UUID
    libro_id: UUID
    pagina: int
    cita: str
    nota: Optional[str] = None
    fecha: datetime = Field(default_factory=datetime.utcnow)