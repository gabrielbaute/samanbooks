from uuid import uuid4, UUID
from typing import Optional, List, Dict
from datetime import date

from app.domain.services import AutorService
from app.domain.entities import Autor
from app.domain.exceptions import MetadatosIncompletos, AutorNoValido, AutorNoEncontrado
from app.infrastructure.database.repositories.sqlalchemy_autor_repository import SQLAlchemyAutorRepository

class AutorServiceImpl(AutorService):
    def __init__(self, autor_repo: SQLAlchemyAutorRepository):
        self.repo = autor_repo
    
    def registrar_autor(
        self,
        nombre: str,
        foto_hash: Optional[str] = None,
        biografia: Optional[str] = None,
        fecha_nacimiento: Optional[date] = None,
        fecha_muerte: Optional[date] = None,
        nacionalidad: Optional[str] = None,
        redes_sociales: Optional[Dict[str, str]] = None,
        libros: Optional[List[UUID]] = None
        ) -> Autor:
        if not nombre:
            raise MetadatosIncompletos()
        
        autor = Autor(
            id=uuid4(),
            nombre=nombre,
            foto_hash=foto_hash,
            biografia=biografia,
            fecha_nacimiento=fecha_nacimiento,
            fecha_muerte=fecha_muerte,
            nacionalidad=nacionalidad,
            redes_sociales=redes_sociales,
            libros=libros
        )
        try:
            self.repo.guardar(autor)
        except Exception as e:
            raise AutorNoValido(f"Error al crear el autor: {e}")
        return autor
    
    def obtener_por_id(self, autor_id: UUID) -> Autor:
        autor = self.repo.obtener_por_id(autor_id)
        if not autor:
            raise AutorNoEncontrado()
        return autor
    
    def buscar_por_nombre(self, nombre) -> List[Autor]:
        autores = self.repo.buscar_por_nombre(nombre)
        if not autores:
            raise AutorNoEncontrado()
        return autores
    
    def obtener_todos(self) -> List[Autor]:
        return self.repo.listar_todos()
    
    def editar_metadata_autor(self, autor_id, metadatos) -> Optional[bool]:
        try:
            autor = self.repo.obtener_por_id(autor_id)
            if not autor:
                return False

            for campo in ["nombre", "foto_hash", "biografia", "fecha_nacimiento", "fecha_muerte", "nacionalidad", "redes_sociales"]:
                if campo in metadatos:
                    setattr(autor, campo, metadatos[campo])

            self.repo.guardar(autor)
            return True
        except Exception as e:
            return False

    def buscar_o_crear_por_nombre(self, nombre) -> Autor:
        try:
            return self.buscar_por_nombre(nombre)[0]
        except AutorNoEncontrado:
            return self.registrar_autor(nombre)

    def eliminar(self, autor_id: UUID) -> None:
        self.repo.eliminar(autor_id)