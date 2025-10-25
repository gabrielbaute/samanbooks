from uuid import uuid4, UUID
from typing import Optional, List, Dict

from domain.entities  import Marcador
from domain.repositories import MarcadorRepository
from domain.exceptions import MarcadorNoEncontrado, MarcadorInvalido

class MarcadorService:
    def __init__(self, marcador_repo: MarcadorRepository):
        self.repo = marcador_repo

    def crear_marcador(self, usuario_id: UUID, libro_id: UUID, pagina: int, capitulo: Optional[str] = None, porcentaje: Optional[float] = None) -> Marcador:
        """
        Crea un nuevo marcador para un usuario en un libro.

        Args:
            usuario_id (UUID): El ID del usuario.
            libro_id (UUID): El ID del libro.
            pagina (int): La página del marcador.
            capitulo (Optional[str]): El capítulo del marcador.
            porcentaje (Optional[float]): El porcentaje de lectura en el marcador.

        Returns:
            Marcador: El marcador creado.
        """
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


    def obtener_marcadores_por_usuario_y_libro(self, usuario_id: UUID, libro_id: UUID) -> List[Marcador]:
        """
        Obtiene todos los marcadores de un usuario para un libro específico.

        Args:
            usuario_id (UUID): El ID del usuario.
            libro_id (UUID): El ID del libro.

        Returns:
            List[Marcador]: Una lista de marcadores.
        """
        marcadores = []
        for marcador in self.repo.obtener_por_usuario(usuario_id):
            if marcador.libro_id == libro_id:
                marcadores.append(marcador)
        return marcadores

    def obtener_marcador_por_id(self, marcador_id: UUID) -> Optional[Marcador]:
        """
        Obtiene un marcador por su ID.

        Args:
            marcador_id (UUID): El ID del marcador.

        Returns:
            Optional[Marcador]: El marcador encontrado, o None si no existe.
        """
        return self.repo.obtener_por_id(marcador_id)

    def obtener_marcador_por_usuario(self, usuario_id: UUID) -> List[Marcador]:
        """
        Obtiene todos los marcadores de un usuario.

        Args:
            usuario_id (UUID): El ID del usuario.

        Returns:
            List[Marcador]: Una lista de marcadores.
        """
        return self.repo.obtener_por_usuario(usuario_id)

    def editar_nota_de_marcador(self, marcador_id: UUID, nota: str) -> Marcador:
        """
        Edita la nota de un marcador.

        Args:
            marcador_id (UUID): El ID del marcador.
            nota (str): La nueva nota del marcador.

        Returns:
            Marcador: El marcador editado.
        """
        marcador = self.obtener_marcador_por_id(marcador_id)
        if not marcador:
            raise MarcadorNoEncontrado()
        marcador.nota = nota
        self.repo.guardar(marcador)
        return marcador

    def eliminar_marcador(self, marcador_id: UUID) -> None:
        """
        Elimina un marcador por su ID.

        Args:
            marcador_id (UUID): El ID del marcador.
        """
        self.repo.eliminar(marcador_id)