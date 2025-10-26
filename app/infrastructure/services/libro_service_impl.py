from uuid import uuid4, UUID
from typing import Optional, List, Dict

from app.domain.services import LibroService
from app.domain.entities import Libro
from app.domain.enums import Formato
from app.domain.exceptions import MetadatosIncompletos, LibroNoValido, LibroNoEncontrado
from app.infrastructure.database.repositories.sqlalchemy_libro_repository import SQLAlchemyLibroRepository

class LibroServiceImpl(LibroService):
    def __init__(self, libro_repo: SQLAlchemyLibroRepository):
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
        libro = self.repo.obtener_por_id(libro_id)
        if not libro:
            raise LibroNoEncontrado()
        return libro

    def buscar_por_autor(self, autor_id) -> List[Libro]:
        libros = self.repo.buscar_por_autor(autor_id)
        if not libros:
            raise LibroNoEncontrado()
        return libros
    
    def buscar_por_serie(self, serie_id) -> List[Libro]:
        return self.repo.buscar_por_serie(serie_id)

    def obtener_todos(self) -> List[Libro]:
        return self.repo.listar_todos()

    def eliminar(self, libro_id: UUID) -> None:
        self.repo.eliminar(libro_id)
    
    def editar_metadata_libro(self, libro_id, metadatos) -> Optional[bool]:
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