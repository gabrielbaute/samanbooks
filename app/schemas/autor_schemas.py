from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional, Dict
from uuid import UUID

class AutorSchemaCreate(BaseModel):
    nombre: str
    foto_hash: Optional[str] = None
    libros: Optional[List[UUID]] = Field(default_factory=list)
    series: Optional[List[UUID]] = Field(default_factory=list)
    fecha_nacimiento: Optional[date] = None
    fecha_fallecimiento: Optional[date] = None
    nacionalidad: Optional[str] = None
    biografia: Optional[str] = None
    redes_sociales: Optional[Dict[str, str]] = None

class AutorSchemaResponse(BaseModel):
    id: UUID
    nombre: str
    foto_hash: Optional[str] = None
    libros: Optional[List[UUID]] = Field(default_factory=list)
    series: Optional[List[UUID]] = Field(default_factory=list)
    fecha_nacimiento: Optional[date] = None
    fecha_fallecimiento: Optional[date] = None
    nacionalidad: Optional[str] = None
    biografia: Optional[str] = None
    redes_sociales: Optional[Dict[str, str]] = None

class AutorSchemaUpdate(BaseModel):
    nombre: Optional[str] = None
    foto_hash: Optional[str] = None
    libros: Optional[List[UUID]] = Field(default_factory=list)
    series: Optional[List[UUID]] = Field(default_factory=list)
    fecha_nacimiento: Optional[date] = None
    fecha_fallecimiento: Optional[date] = None
    nacionalidad: Optional[str] = None
    biografia: Optional[str] = None
    redes_sociales: Optional[Dict[str, str]] = None
