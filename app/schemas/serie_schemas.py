from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID

class SerieSchemaCreate(BaseModel):
    nombre: str
    autor_ids: List[UUID]
    libros: List[UUID] = Field(default_factory=list)
    descripcion: Optional[str] = None
    portada_hash: Optional[str] = None

class SerieSchemaResponse(BaseModel):
    id: UUID
    nombre: str
    autor_ids: List[UUID]
    libros: List[UUID]
    descripcion: Optional[str] = None
    portada_hash: Optional[str] = None