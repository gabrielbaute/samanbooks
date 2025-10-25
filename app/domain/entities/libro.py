from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List, Optional

from app.domain.enums import Formato

class Libro(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    titulo: str
    autores: List[UUID]
    path: str
    formato: Formato
    portada_hash: str
    isbn: Optional[str] = None
    fecha_publicacion: Optional[str] = None
    editorial: Optional[str] = None
    serie_id: Optional[UUID] = None
    descripcion: Optional[str] = None
    paginas: Optional[int] = None
    year: Optional[int] = None