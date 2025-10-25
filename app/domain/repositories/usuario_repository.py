from abc import ABC, abstractmethod
from uuid import UUID
from domain.entities import Usuario

class UsuarioRepository(ABC):
    @abstractmethod
    def guardar(self, usuario: Usuario) -> None: pass

    @abstractmethod
    def obtener_por_id(self, id: UUID) -> Usuario | None: pass

    @abstractmethod
    def obtener_por_email(self, email: str) -> Usuario | None: pass

    @abstractmethod
    def eliminar(self, id: UUID) -> None: pass

    @abstractmethod
    def listar_todos(self) -> list[Usuario]: pass


