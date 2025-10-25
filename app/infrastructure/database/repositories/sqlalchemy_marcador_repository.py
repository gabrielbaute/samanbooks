from uuid import UUID
from typing import List, Optional
from datetime import datetime

from domain.entities import Marcador
from domain.repositories import MarcadorRepository
from infrastructure.database.models.marcador_model import MarcadorModel

class SQLAlchemyMarcadorRepository(MarcadorRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, marcador: Marcador) -> None:
        """
        Guarda un marcador en la base de datos.

        Args:
            marcador (Marcador): El marcador a guardar.
        """
        modelo = MarcadorModel(
            id=marcador.id,
            usuario_id=marcador.usuario_id,
            libro_id=marcador.libro_id,
            pagina=marcador.pagina,
            cita=marcador.cita,
            nota=marcador.nota,
            fecha=marcador.fecha
        )
        self.session.add(modelo)
        self.session.commit()

    def obtener_por_id(self, id: UUID) -> Optional[Marcador]:
        """
        Obtiene un marcador por su ID.

        Args:
            id (UUID): El ID del marcador.

        Returns:
            Optional[Marcador]: El marcador encontrado o None si no se encuentra.
        """
        modelo = self.session.get(MarcadorModel, id)
        return Marcador(**modelo.__dict__) if modelo else None

    def obtener_por_usuario(self, usuario_id: UUID) -> List[Marcador]:
        """
        Obtiene marcadores por usuario.

        Args:
            usuario_id (UUID): El ID del usuario.

        Returns:
            List[Marcador]: Una lista de marcadores del usuario.
        """
        resultados = (
            self.session.query(MarcadorModel)
            .filter_by(usuario_id=usuario_id)
            .all()
        )
        return [Marcador(**r.__dict__) for r in resultados]

    def obtener_por_libro(self, libro_id: UUID) -> List[Marcador]:
        """
        Obtiene marcadores por libro.

        Args:
            libro_id (UUID): El ID del libro.

        Returns:
            List[Marcador]: Una lista de marcadores del libro.
        """
        resultados = (
            self.session.query(MarcadorModel)
            .filter_by(libro_id=libro_id)
            .all()
        )
        return [Marcador(**r.__dict__) for r in resultados]

    def listar_todos(self) -> List[Marcador]:
        """
        Obtiene una lista de todos los marcadores.

        Returns:
            List[Marcador]: Una lista de todos los marcadores.
        """
        resultados = self.session.query(MarcadorModel).all()
        return [Marcador(**r.__dict__) for r in resultados]

    def eliminar(self, id: UUID) -> Optional[bool]:
        """
        Elimina un marcador por su ID.

        Args:
            id (UUID): El ID del marcador.
        
        Returns:
            Optional[bool]: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            self.session.query(MarcadorModel).filter_by(id=id).delete()
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            return False
        finally:
            self.session.close()