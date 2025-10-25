from uuid import uuid4, UUID
from typing import Optional, List, Dict

from domain.entities import Libro
from domain.enums import Formato
from domain.repositories import LibroRepository
from domain.exceptions import MetadatosIncompletos, LibroNoValido, LibroNoEncontrado

class LibroService:
    def __init__(self, libro_repo: LibroRepository):
        self.repo = libro_repo

    def registrar_libro(
            self,
            titulo: str,
            autores: List[UUID],
            path: str,
            formato: Formato,
            portada_hash: str,
            isbn: Optional[str] = None,
            fecha_publicacion: Optional[str] = None,
            editorial: Optional[str] = None,
            serie_id: Optional[UUID] = None,
            descripcion: Optional[str] = None,
            paginas: Optional[int] = None,
            year: Optional[int] = None
    ) -> Libro:
        """
        Registra un nuevo libro.

        Args:
            titulo (str): El título del libro.
            autores (List[UUID]): La lista de IDs de los autores del libro.
            path (str): La ruta del archivo del libro.
            formato (Formato): El formato del libro.
            portada_hash (str): El hash de la portada del libro.
            isbn (Optional[str]): El ISBN del libro.
            fecha_publicacion (Optional[str]): La fecha de publicación del libro.
            editorial (Optional[str]): La editorial del libro.
            serie_id (Optional[UUID]): El ID de la serie a la que pertenece el libro.
            descripcion (Optional[str]): La descripción del libro.
            paginas (Optional[int]): El número de páginas del libro.
            year (Optional[int]): El año de publicación del libro.

        Returns:
            Libro: El libro registrado.

        Raises:
            MetadatosIncompletos: Si faltan metadatos obligatorios.
            LibroNoValido: Si el libro no es válido.
        """
        if not titulo or not autores or not path or not formato or not portada_hash:
            raise MetadatosIncompletos()

        libro = Libro(
            id=uuid4(),
            titulo=titulo,
            autores=autores,
            path=path,
            formato=formato,
            portada_hash=portada_hash,
            isbn=isbn,
            fecha_publicacion=fecha_publicacion,
            editorial=editorial,
            serie_id=serie_id,
            descripcion=descripcion,
            paginas=paginas,
            year=year
        )
        try:
            self.repo.guardar(libro)
        except Exception as e:
            raise LibroNoValido(f"Error al crear el libro: {e}")
        return libro
    
    def obtener_por_id(self, libro_id: UUID) -> Libro:
        """
        Obtiene un libro por su ID.

        Args:
            libro_id (UUID): El ID del libro.

        Returns:
            Libro: El libro encontrado.

        Raises:
            LibroNoEncontrado: Si no se encuentra el libro.
        """
        libro = self.repo.obtener_por_id(libro_id)
        if not libro:
            raise LibroNoEncontrado()
        return libro
    
    def buscar_por_autor(self, autor_id: UUID) -> List[Libro]:
        """
        Busca libros por autor.

        Args:
            autor_id (UUID): El ID del autor.

        Returns:
            List[Libro]: La lista de libros encontrados.

        Raises:
            LibroNoEncontrado: Si no se encuentran libros para el autor.
        """
        libros = self.repo.buscar_por_autor(autor_id)
        if not libros:
            raise LibroNoEncontrado()
        return libros

    
    def buscar_por_serie(self, serie_id: UUID) -> List[Libro]:
        """
        Busca libros por serie.

        Args:
            serie_id (UUID): El ID de la serie.

        Returns:
            List[Libro]: La lista de libros encontrados.
        """
        return self.repo.buscar_por_serie(serie_id)

    def obtener_todos(self) -> List[Libro]:
        """
        Obtiene todos los libros.

        Returns:
            List[Libro]: La lista de libros.
        """
        return self.repo.listar_todos()

    def eliminar(self, libro_id: UUID) -> None:
        """
        Elimina un libro por su ID.

        Args:
            libro_id (UUID): El ID del libro.
        """
        self.repo.eliminar(libro_id)
    
    def editar_metadata_libro(self, libro_id: UUID, metadatos: Dict) -> Optional[bool]:
        """
        Edita los metadatos de un libro.

        Args:
            libro_id (UUID): El ID del libro.
            metadatos (dict): Los metadatos a editar.

        Returns:
            Optional[bool]: True si la edición se realizó correctamente, False en caso contrario.
        """
        try:
            libro = self.repo.obtener_por_id(libro_id)
            if not libro:
                return False

            for campo in ["titulo", "descripcion", "paginas", "year", "serie_id", "portada_hash"]:
                if campo in metadatos:
                    setattr(libro, campo, metadatos[campo])

            self.repo.guardar(libro)
            return True
        except Exception as e:
            return False