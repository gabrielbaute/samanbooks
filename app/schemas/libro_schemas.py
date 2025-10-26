from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

from app.domain.enums import Formato

class LibroCreateSchema(BaseModel):
    titulo: str
    autores: List[UUID]
    path: str
    formato: Formato
    portada_hash: str
    isbn: Optional[str]
    fecha_publicacion: Optional[str]
    editorial: Optional[str]
    serie_id: Optional[UUID]
    descripcion: Optional[str]
    paginas: Optional[int]
    year: Optional[int]

class LibroResponseSchema(BaseModel):
    id: UUID
    titulo: str
    autores: List[UUID]
    path: str
    formato: Formato
    portada_hash: str
    isbn: Optional[str]
    serie_id: Optional[UUID]
    descripcion: Optional[str]
    paginas: Optional[int]
    year: Optional[int]
    fecha_publicacion: Optional[str]
    editorial: Optional[str]

class LibroUpdateSchema(BaseModel):
    titulo: Optional[str] = None
    autores: Optional[List[UUID]] = None
    path: Optional[str] = None
    formato: Optional[Formato] = None
    portada_hash: Optional[str] = None
    isbn: Optional[str] = None
    fecha_publicacion: Optional[str] = None
    editorial: Optional[str] = None
    serie_id: Optional[UUID] = None
    descripcion: Optional[str] = None
    paginas: Optional[int] = None
    year: Optional[int] = None