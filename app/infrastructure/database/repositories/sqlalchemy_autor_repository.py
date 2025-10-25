from uuid import UUID
from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy

from domain.entities.autor import Autor
from domain.repositories.autor_repository import AutorRepository
from infrastructure.database.models.autor_model import AutorModel

class SQLAlchemyAutorRepository(AutorRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, autor: Autor) -> None:
        """
        Guarda un autor en la base de datos.

        Args:
            autor (Autor): El autor a guardar.
        """
        modelo = AutorModel(
            id=autor.id,
            nombre=autor.nombre,
            foto_path=autor.foto_hash,
            biografia=autor.biografia,
            fecha_nacimiento=autor.fecha_nacimiento,
            fecha_muerte=autor.fecha_muerte,
            nacionalidad=autor.nacionalidad,
            redes_sociales=autor.redes_sociales,
            libros=autor.libros
        )
        self.session.add(modelo)
        self.session.commit()

    def obtener_por_id(self, id: UUID) -> Optional[Autor]:
        """
        Obtiene un autor por su ID.

        Args:
            id (UUID): El ID del autor.

        Returns:
            Optional[Autor]: El autor encontrado o None si no se encuentra.
        """
        modelo = self.session.get(AutorModel, id)
        return Autor(**modelo.__dict__) if modelo else None

    def buscar_por_nombre(self, nombre: str) -> List[Autor]:
        """
        Busca autores por nombre.

        Args:
            nombre (str): El nombre del autor.

        Returns:
            List[Autor]: Una lista de autores que coinciden con el nombre.
        """
        resultados = (
            self.session.query(AutorModel)
            .filter(AutorModel.nombre.ilike(f"%{nombre}%"))
            .all()
        )
        return [Autor(**r.__dict__) for r in resultados]

    def listar_todos(self) -> List[Autor]:
        """
        Obtiene una lista de todos los autores.

        Returns:
            List[Autor]: Una lista de todos los autores.
        """
        resultados = self.session.query(AutorModel).all()
        return [Autor(**r.__dict__) for r in resultados]

    def eliminar(self, id: UUID) -> Optional[bool]:
        """
        Elimina un autor por su ID.

        Args:
            id (UUID): El ID del autor.
        """
        try:
            self.session.query(AutorModel).filter_by(id=id).delete()
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            return False
        finally:
            self.session.close()