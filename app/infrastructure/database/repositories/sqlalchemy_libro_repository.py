from domain.entities.libro import Libro
from domain.repositories.libro_repository import LibroRepository
from infrastructure.database.models.libro_model import LibroModel, libros_autores

from uuid import UUID
from typing import List, Optional

class SQLAlchemyLibroRepository(LibroRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, libro: Libro) -> None:
        """
        Guarda un libro en la base de datos.

        Args:
            libro (Libro): El libro a guardar.
        """
        modelo = LibroModel(
            id=libro.id,
            titulo=libro.titulo,
            path=libro.path,
            formato=libro.formato.value,
            portada_hash=libro.portada_hash,
            isbn=libro.isbn,
            fecha_publicacion=libro.fecha_publicacion,
            editorial=libro.editorial,
            descripcion=libro.descripcion,
            paginas=libro.paginas,
            year=libro.year,
            serie_id=libro.serie_id
        )
        self.session.add(modelo)
        self.session.commit()

        # Relación autores (N:M)
        for autor_id in libro.autores:
            self.session.execute(libros_autores.insert().values(
                libro_id=libro.id,
                autor_id=autor_id
            ))
        self.session.commit()

    def obtener_por_id(self, id: UUID) -> Optional[Libro]:
        """
        Obtiene un libro por su ID.

        Args:
            id (UUID): El ID del libro.

        Returns:
            Optional[Libro]: El libro encontrado o None si no se encuentra.
        """
        modelo = self.session.get(LibroModel, id)
        return Libro(**modelo.__dict__) if modelo else None

    def buscar_por_autor(self, autor_id: UUID) -> List[Libro]:
        """
        Busca libros por autor.

        Args:
            autor_id (UUID): El ID del autor.

        Returns:
            List[Libro]: Una lista de libros que corresponden al autor.
        """
        resultados = (
            self.session.query(LibroModel)
            .join(libros_autores)
            .filter(libros_autores.c.autor_id == autor_id)
            .all()
        )
        return [Libro(**r.__dict__) for r in resultados]

    def buscar_por_serie(self, serie_id: UUID) -> List[Libro]:
        """
        Busca libros por serie.
        
        Args:
            serie_id (UUID): El ID de la serie.

        Returns:
            List[Libro]: Una lista de libros que corresponden a la serie.
        """
        resultados = (
            self.session.query(LibroModel)
            .filter_by(serie_id=serie_id)
            .all()
        )
        return [Libro(**r.__dict__) for r in resultados]

    def eliminar(self, id: UUID) -> Optional[bool]:
        """
        Elimina un libro por su ID.

        Args:
            id (UUID): El ID del libro.
        """
        try:
            self.session.query(LibroModel).filter_by(id=id).delete()
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            return False
        finally:
            self.session.close()

    def listar_todos(self) -> List[Libro]:
        """
        Obtiene una lista de todos los libros.

        Returns:
            List[Libro]: Una lista de todos los libros.
        """
        resultados = self.session.query(LibroModel).all()
        return [Libro(**r.__dict__) for r in resultados]
    
    def buscar_por_titulo(self, titulo: str) -> List[Libro]:
        """
        Busca libros por título.

        Args:
            titulo (str): El título del libro.

        Returns:
            List[Libro]: Una lista de libros que coinciden con el título.
        """
        resultados = (
            self.session.query(LibroModel)
            .filter(LibroModel.titulo.ilike(f"%{titulo}%"))
            .all()
        )
        return [Libro(**r.__dict__) for r in resultados]
