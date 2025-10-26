from uuid import uuid4, UUID
from typing import Optional, List

from app.domain.services import SerieService
from app.domain.entities import Serie
from app.domain.exceptions import MetadatosIncompletos, SerieInvalida, SerieNoEncontrada
from app.infrastructure.database.repositories.sqlalchemy_serie_repository import SQLAlchemySerieRepository

class SerieServiceImpl(SerieService):
    def __init__(self, serie_repo: SQLAlchemySerieRepository):
        self.repo = serie_repo

    def registrar_serie(
            self,
            nombre: str,
            autor_ids: List[UUID],
            libros: List[UUID],
            descripcion: Optional[str] = None,
            portada_hash: Optional[str] = None
    ) -> Serie:
        if not nombre or not autor_ids or not libros:
            raise MetadatosIncompletos()
        
        serie = Serie(
            id=uuid4(),
            nombre=nombre,
            autor_ids=autor_ids,
            libros=libros,
            descripcion=descripcion,
            portada_hash=portada_hash
        )
        try:
            self.repo.guardar(serie)
        except Exception as e:
            raise SerieInvalida(f"Error al crear la serie: {e}")
        return serie
    
    def obtener_por_id(self, serie_id: UUID) -> Serie:
        serie = self.repo.obtener_por_id(serie_id)
        if not serie:
            raise SerieNoEncontrada()
        return serie
    
    def buscar_por_autor(self, autor_id: UUID) -> List[Serie]:
        series = self.repo.buscar_por_autor(autor_id)
        if not series:
            raise SerieNoEncontrada()
        return series

    def buscar_por_nombre(self, nombre: str) -> List[Serie]:
        series = self.repo.buscar_por_nombre(nombre)
        if not series:
            raise SerieNoEncontrada()
        return series

    def buscar_o_crear_por_nombre(self, nombre: str) -> Serie:
        try:
            return self.buscar_por_nombre(nombre)[0]
        except SerieNoEncontrada:
            return self.registrar_serie(nombre)
    
    def agregar_libro_a_serie(self, serie_id, libro_id) -> Optional[bool]:
        try:
            serie = self.repo.obtener_por_id(serie_id)
            if not serie:
                return False

            serie.libros.append(libro_id)
            self.repo.guardar(serie)
            return True
        except Exception as e:
            return False
    
    def retirar_un_libro_de_una_serie(self, serie_id, libro_id) -> Optional[bool]:
        try:
            serie = self.repo.obtener_por_id(serie_id)
            if not serie:
                return False

            serie.libros.remove(libro_id)
            self.repo.guardar(serie)
            return True
        except Exception as e:
            return False
        
    def eliminar_serie(self, serie_id) -> None:
        self.repo.eliminar(serie_id)