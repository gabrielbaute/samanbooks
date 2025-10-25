from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import date

class Autor(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    nombre: str
    foto_hash: Optional[str] = None
    biografia: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    fecha_muerte: Optional[date] = None
    nacionalidad: Optional[str] = None
    redes_sociales: Optional[Dict[str, str]] = None
    libros: Optional[List[UUID]] = None