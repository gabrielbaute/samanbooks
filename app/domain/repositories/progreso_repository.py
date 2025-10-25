from typing import List, Optional
from abc import ABC, abstractmethod
from uuid import UUID
from domain.entities import Progreso

class ProgresoRepository(ABC):
    @abstractmethod
    def guardar(self, progreso: Progreso) -> None: pass

    @abstractmethod
    def obtener_por_usuario_y_libro(self, usuario_id: UUID, libro_id: UUID) -> Optional[Progreso]: pass

    @abstractmethod
    def actualizar_estatus(self, usuario_id: UUID, libro_id: UUID, nuevo_estatus: str) -> None: pass

    @abstractmethod
    def eliminar(self, id: UUID) -> None: pass

    @abstractmethod
    def listar_todos(self) -> List[Progreso]: pass

    @abstractmethod
    def obtener_por_id(self, id: UUID) -> Optional[Progreso]: pass