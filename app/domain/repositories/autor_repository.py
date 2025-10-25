from typing import List, Optional
from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities import Autor

class AutorRepository(ABC):
    @abstractmethod
    def guardar(self, autor: Autor) -> None: pass

    @abstractmethod
    def obtener_por_id(self, id: UUID) -> Optional[Autor]: pass

    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Autor]: pass

    @abstractmethod
    def eliminar(self, id: UUID) -> None: pass

    @abstractmethod
    def listar_todos(self) -> List[Autor]: pass