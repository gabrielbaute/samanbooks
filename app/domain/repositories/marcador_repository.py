from typing import List, Optional
from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities import Marcador

class MarcadorRepository(ABC):
    @abstractmethod
    def guardar(self, marcador: Marcador) -> None: pass

    @abstractmethod
    def obtener_por_usuario(self, usuario_id: UUID) -> List[Marcador]: pass

    @abstractmethod
    def obtener_por_libro(self, libro_id: UUID) -> List[Marcador]: pass

    @abstractmethod
    def eliminar(self, id: UUID) -> None: pass

    @abstractmethod
    def listar_todos(self) -> List[Marcador]: pass

    @abstractmethod
    def obtener_por_id(self, id: UUID) ->Optional[Marcador]: pass