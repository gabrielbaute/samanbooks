from typing import List, Optional
from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities import Libro

class LibroRepository(ABC):
    @abstractmethod
    def guardar(self, libro: Libro) -> None: pass

    @abstractmethod
    def obtener_por_id(self, id: UUID) -> Optional[Libro]: pass

    @abstractmethod
    def buscar_por_autor(self, autor_id: UUID) -> List[Libro]: pass

    @abstractmethod
    def buscar_por_serie(self, serie_id: UUID) -> List[Libro]: pass

    @abstractmethod
    def eliminar(self, id: UUID) -> None: pass

    @abstractmethod
    def listar_todos(self) -> List[Libro]: pass
