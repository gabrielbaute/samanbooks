from domain.entities import Serie
from domain.repositories import SerieRepository
from infrastructure.database.models.serie_model import SerieModel

from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy
from uuid import UUID

class SQLAlchemySerieRepository(SerieRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, serie: Serie) -> None:
        """
        Guarda una serie en la base de datos.

        Args:
            serie (Serie): La serie a guardar.
        """
        modelo = SerieModel(
            id=serie.id,
            nombre=serie.nombre,
            descripcion=serie.descripcion,
            portada_hash=serie.portada_hash,
            autor_id=serie.autor_id,
            libros=serie.libros
        )
        self.session.add(modelo)
        self.session.commit()

    def obtener_por_id(self, id: UUID) -> Optional[Serie]:
        """
        Obtiene una serie por su ID.

        Args:
            id (UUID): El ID de la serie.

        Returns:
            Optional[Serie]: La serie encontrada o None si no se encuentra.
        """
        modelo = self.session.get(SerieModel, id)
        return Serie(**modelo.__dict__) if modelo else None

    def buscar_por_nombre(self, nombre: str) -> List[Serie]:
        """
        Busca series por nombre.

        Args:
            nombre (str): El nombre de la serie.

        Returns:
            List[Serie]: Una lista de series que coinciden con el nombre.
        """
        resultados = (
            self.session.query(SerieModel)
            .filter(SerieModel.nombre.ilike(f"%{nombre}%"))
            .all()
        )
        return [Serie(**r.__dict__) for r in resultados]
    
    def buscar_por_autor(self, autor_id: UUID) -> List[Serie]:
        """
        Busca series por autor.

        Args:
            autor_id (UUID): El ID del autor.

        Returns:
            List[Serie]: Una lista de series que corresponden al autor.
        """
        resultados = (
            self.session.query(SerieModel)
            .filter_by(autor_id=autor_id)
            .all()
        )
        return [Serie(**r.__dict__) for r in resultados]

    def eliminar(self, id: UUID) -> None:
        """
        Elimina una serie por su ID.

        Args:
            id (UUID): El ID de la serie.
        """
        self.session.query(SerieModel).filter_by(id=id).delete()
        self.session.commit()

    def listar_todos(self) -> List[Serie]:
        """
        Obtiene una lista de todas las series.

        Returns:
            List[Serie]: Una lista de todas las series.
        """
        resultados = self.session.query(SerieModel).all()
        return [Serie(**r.__dict__) for r in resultados]
