from uuid import uuid4, UUID
from typing import Optional, List, Dict
from datetime import date

from app.domain.services import MarcadorService
from app.domain.entities import Marcador
from app.domain.enums import Estatus
from app.domain.exceptions import MetadatosIncompletos, MarcadorInvalido, MarcadorNoEncontrado
from app.infrastructure.database.repositories.sqlalchemy_marcador_repository import SQLAlchemyMarcadorRepository

class MarcadorServiceImpl(MarcadorService):
    def __init__(self, marcador_repo: SQLAlchemyMarcadorRepository):
        self.repo = marcador_repo

    def crear_marcador(
            self, 
            usuario_id: UUID, 
            libro_id: UUID, 
            pagina: int, 
            capitulo: Optional[str] = None, 
            porcentaje: Optional[float] = None
        ) -> Marcador:
        if not usuario_id or not libro_id or not pagina:
            raise MetadatosIncompletos()

        marcador = Marcador(
            id=uuid4(),
            usuario_id=usuario_id,
            libro_id=libro_id,
            pagina=pagina,
            capitulo=capitulo,
            porcentaje=porcentaje
        )

        try:
            self.repo.guardar(marcador)
        except Exception as e:
            raise MarcadorInvalido(f"Error al crear el marcador: {e}")
        return marcador
    
    def obtener_marcadores_por_usuario_y_libro(self, usuario_id, libro_id) -> List[Marcador]:
        marcadores = []
        for marcador in self.repo.obtener_por_usuario(usuario_id):
            if marcador.libro_id == libro_id:
                marcadores.append(marcador)
        return marcadores
    
    def obtener_marcador_por_id(self, marcador_id: UUID) -> Optional[Marcador]:
        return self.repo.obtener_por_id(marcador_id)

    def obtener_marcador_por_usuario(self, usuario_id: UUID) -> List[Marcador]:
        return self.repo.obtener_por_usuario(usuario_id)
    
    def editar_nota_de_marcador(self, marcador_id: UUID, nota: str) -> Marcador:
        marcador = self.obtener_marcador_por_id(marcador_id)
        if not marcador:
            raise MarcadorNoEncontrado()
        marcador.nota = nota
        self.repo.guardar(marcador)
        return marcador
    
    def eliminar_marcador(self, marcador_id) -> None:
        self.repo.eliminar(marcador_id)
    
    def listar_todos(self) -> List[Marcador]:
        return self.repo.listar_todos()