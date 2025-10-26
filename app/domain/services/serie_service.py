from uuid import uuid4, UUID
from typing import Optional, List, Dict

from domain.entities import Serie
from domain.repositories import SerieRepository
from domain.exceptions import SerieNoEncontrada, SerieInvalida

class SerieService:
    def __init__(self, serie_repo: SerieRepository):
        self.repo = serie_repo
    
    def registrar_serie(
            self,
            nombre: str,
            autor_ids: List[UUID],
            libros: List[UUID],
            descripcion: Optional[str] = None,
            portada_hash: Optional[str] = None
    ) -> Serie:
        """
        Registra una nueva serie.

        Args:
            nombre (str): El título de la serie.
            autor_ids (List[UUID]): La lista de IDs de los autores de la serie.
            libros (List[UUID]): La lista de IDs de los libros de la serie.
            descripcion (Optional[str]): La descripción de la serie.
            portada_hash (Optional[str]): El hash de la portada de la serie.

        Returns:
            Serie: La serie registrada.

        Raises:
            SerieInvalida: Si la serie no es válida.
        """
        serie = Serie(
            id=uuid4(),
            nombre=nombre,
            autor_ids=autor_ids,
            libros=libros,
            descripcion=descripcion,
            portada_hash=portada_hash
        )
    
    def obtener_por_id(self, serie_id: UUID) -> Serie:
        """
        Obtiene una serie por su ID.

        Args:
            serie_id (UUID): El ID de la serie.

        Returns:
            Serie: La serie encontrada.

        Raises:
            SerieNoEncontrada: Si no se encuentra la serie.
        """
        serie = self.repo.obtener_por_id(serie_id)
        if not serie:
            raise SerieNoEncontrada()
        return serie
    
    def buscar_por_autor(self, autor_id: UUID) -> List[Serie]:
        """
        Busca series por autor.

        Args:
            autor_id (UUID): El ID del autor.

        Returns:
            List[Serie]: La lista de series encontradas.

        Raises:
            SerieNoEncontrada: Si no se encuentran series para el autor.
        """
        series = self.repo.buscar_por_autor(autor_id)
        if not series:
            raise SerieNoEncontrada()
        return series
    
    def agregar_libro_a_serie(self, serie_id: UUID, libro_id: UUID) -> Optional[bool]:
        """
        Agrega un libro a una serie.

        Args:
            serie_id (UUID): El ID de la serie.
            libro_id (UUID): El ID del libro.

        Returns:
            Optional[bool]: True si el libro se agregó correctamente, False en caso contrario.
        """
        try:
            serie = self.repo.obtener_por_id(serie_id)
            if not serie:
                return False

            serie.libros.append(libro_id)
            self.repo.guardar(serie)
            return True
        except Exception as e:
            return False
        
    def retirar_un_libro_de_una_serie(self, serie_id: UUID, libro_id: UUID) -> Optional[bool]:
        """
        Retira un libro de una serie.

        Args:
            serie_id (UUID): El ID de la serie.
            libro_id (UUID): El ID del libro.

        Returns:
            Optional[bool]: True si el libro se retiró correctamente, False en caso contrario.
        """
        try:
            serie = self.repo.obtener_por_id(serie_id)
            if not serie:
                return False

            serie.libros.remove(libro_id)
            self.repo.guardar(serie)
            return True
        except Exception as e:
            return False
    
    def eliminar_serie(self, serie_id: UUID) -> None:
        """
        Elimina una serie por su ID.

        Args:
            serie_id (UUID): El ID de la serie.
        """
        self.repo.eliminar(serie_id)