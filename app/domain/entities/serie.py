from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4

class Serie(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    nombre: str
    autor_ids: List[UUID]
    libros: List[UUID]
    descripcion: Optional[str] = None
    portada_hash: Optional[str] = None