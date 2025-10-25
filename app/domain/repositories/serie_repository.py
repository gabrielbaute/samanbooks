from typing import List, Optional
from abc import ABC, abstractmethod
from uuid import UUID
from domain.entities import Serie

class SerieRepository(ABC):
    @abstractmethod
    def guardar(self, serie: Serie) -> None: pass

    @abstractmethod
    def obtener_por_id(self, id: UUID) -> Optional[Serie]: pass

    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Serie]: pass

    @abstractmethod
    def eliminar(self, id: UUID) -> None: pass

    @abstractmethod
    def listar_todos(self) -> List[Serie]: pass