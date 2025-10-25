import uuid
from uuid import UUID
from typing import List, Optional
from datetime import datetime

from domain.entities import Progreso
from domain.repositories import ProgresoRepository
from infrastructure.database.models.progreso_model import ProgresoModel

class SQLAlchemyProgresoRepository(ProgresoRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, progreso: Progreso) -> None:
        """
        Guarda un progreso en la base de datos.

        Args:
            progreso (Progreso): El progreso a guardar.
        """
        modelo = ProgresoModel(
            id=uuid.uuid4(),
            usuario_id=progreso.usuario_id,
            libro_id=progreso.libro_id,
            porcentaje=progreso.porcentaje,
            estatus=progreso.estatus,
            ultima_fecha=progreso.ultima_fecha
        )
        self.session.add(modelo)
        self.session.commit()

    def obtener_por_usuario_y_libro(self, usuario_id: UUID, libro_id: UUID) -> Optional[Progreso]:
        """
        Obtiene un progreso por usuario y libro.

        Args:
            usuario_id (UUID): El ID del usuario.
            libro_id (UUID): El ID del libro.

        Returns:
            Optional[Progreso]: El progreso encontrado o None si no se encuentra.
        """
        modelo = (
            self.session.query(ProgresoModel)
            .filter_by(usuario_id=usuario_id, libro_id=libro_id)
            .first()
        )
        return Progreso(**modelo.__dict__) if modelo else None

    def actualizar_estatus(self, usuario_id: UUID, libro_id: UUID, nuevo_estatus: str) -> None:
        """
        Actualiza el estatus de un progreso.

        Args:
            usuario_id (UUID): El ID del usuario.
            libro_id (UUID): El ID del libro.
            nuevo_estatus (str): El nuevo estatus.
        """
        self.session.query(ProgresoModel).filter_by(
            usuario_id=usuario_id, libro_id=libro_id
        ).update({"estatus": nuevo_estatus, "ultima_fecha": datetime.utcnow()})
        self.session.commit()

    def eliminar(self, id: UUID) -> None:
        """
        Elimina un progreso por su ID.

        Args:
            id (UUID): El ID del progreso.
        """
        self.session.query(ProgresoModel).filter_by(id=id).delete()
        self.session.commit()

    def listar_todos(self) -> List[Progreso]:
        """
        Obtiene una lista de todos los progreso.

        Returns:
            List[Progreso]: Una lista de todos los progreso.
        """
        resultados = self.session.query(ProgresoModel).all()
        return [Progreso(**r.__dict__) for r in resultados]

    def obtener_por_id(self, id: UUID) -> Optional[Progreso]:
        """
        Obtiene un progreso por su ID.

        Args:
            id (UUID): El ID del progreso.
        
        Returns:
            Optional[Progreso]: El progreso encontrado o None si no se encuentra.
        """
        modelo = self.session.get(ProgresoModel, id)
        return Progreso(**modelo.__dict__) if modelo else None
