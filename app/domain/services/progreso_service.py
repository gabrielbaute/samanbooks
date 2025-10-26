from uuid import UUID
from datetime import datetime
from typing import Optional

from domain.entities import Progreso
from domain.enums import Estatus
from domain.repositories import ProgresoRepository
from domain.exceptions import ProgresoInvalido

class ProgresoService:
    def __init__(self, progreso_repo: ProgresoRepository):
        self.repo = progreso_repo

    def actualizar_progreso(self, usuario_id: UUID, libro_id: UUID, porcentaje: float, estatus: Estatus = None) -> None:
        """
        Actualiza el progreso de lectura de un libro para un usuario.

        Args:
            usuario_id (UUID): El ID del usuario.
            libro_id (UUID): El ID del libro.
            porcentaje (float): El porcentaje de lectura.
            estatus (Estatus): El estatus de lectura.

        Raises:
            ProgresoInvalido: Si el porcentaje está fuera de rango.
        """
        if not 0 <= porcentaje <= 100:
            raise ProgresoInvalido("Porcentaje fuera de rango")

        estatus = estatus or (Estatus.TERMINADO if porcentaje == 100 else Estatus.LEYENDO)

        progreso = Progreso(
            usuario_id=usuario_id,
            libro_id=libro_id,
            porcentaje=porcentaje,
            estatus=estatus,
            ultima_fecha=datetime.utcnow()
        )

        self.repo.guardar(progreso)

    def marcar_como_leido(self, usuario_id: UUID, libro_id: UUID) -> bool:
        """
        Marca un libro como leído para un usuario.
        
        Args:
            usuario_id (UUID): El ID del usuario.
            libro_id (UUID): El ID del libro.
        
        Returns:
            bool: True si el progreso se actualizó correctamente, False en caso contrario.
        """
        self.actualizar_progreso(usuario_id, libro_id, 100)
        return True

    def marcar_para_leer_luego(self, usuario_id: UUID, libro_id: UUID) -> bool:
        """
        Marca un libro para leer después para un usuario.

        Args:
            usuario_id (UUID): El ID del usuario.
            libro_id (UUID): El ID del libro.

        Returns:
            bool: True si el estatus se actualizó correctamente, False en caso contrario.
        """
        self.actualizar_progreso(usuario_id, libro_id, 0, Estatus.PENDIENTE)
        return True

    def obtener_progreso(self, usuario_id: UUID, libro_id: UUID) -> Optional[Progreso]:
        """
        Obtiene el progreso de lectura de un libro para un usuario.

        Args:
            usuario_id (UUID): El ID del usuario.
            libro_id (UUID): El ID del libro.

        Returns:
            Optional[Progreso]: El progreso de lectura, o None si no se encuentra.
        """
        return self.repo.obtener_por_usuario_y_libro(usuario_id, libro_id)

    def obtener_progreso_por_id(self, progreso_id: UUID) -> Optional[Progreso]:
        """
        Obtiene el progreso de lectura por su ID.

        Args:
            progreso_id (UUID): El ID del progreso.

        Returns:
            Optional[Progreso]: EL progreso de lectura, None si no se encuentra.
        """
        return self.repo.obtener_por_id(progreso_id)