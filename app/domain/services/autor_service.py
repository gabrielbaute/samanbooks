from uuid import uuid4, UUID
from typing import Optional, List, Dict
from datetime import date

from domain.entities import Autor, Libro
from domain.repositories import AutorRepository
from domain.exceptions import AutorNoEncontrado

class AutorService:
    def __init__(self, autor_repo: AutorRepository):
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
        """
        Registra un nuevo autor.

        Args:
            nombre (str): El nombre del autor.
            foto_hash (Optional[str]): El hash de la foto del autor.
            biografia (Optional[str]): La biografia del autor.
            fecha_nacimiento (Optional[date]): La fecha de nacimiento del autor.
            fecha_muerte (Optional[date]): La fecha de muerte del autor.
            nacionalidad (Optional[str]): La nacionalidad del autor.
            redes_sociales (Optional[Dict[str, str]]): Las redes sociales del autor.
            libros (Optional[List[UUID]]): Los libros escritos por el autor.

        Returns:
            Autor: El autor registrado.
        """
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
        self.repo.guardar(autor)
        return autor

    def obtener_por_id(self, autor_id: UUID) -> Autor:
        """
        Obtiene un autor por su ID.

        Args:
            autor_id (UUID): El ID del autor.

        Returns:
            Autor: El autor encontrado.

        Raises:
            AutorNoEncontrado: Si no se encuentra el autor.
        """
        autor = self.repo.obtener_por_id(autor_id)
        if not autor:
            raise AutorNoEncontrado()
        return autor
    
    def buscar_por_nombre(self, nombre: str) -> List[Autor]:
        """
        Busca autores por nombre.

        Args:
            nombre (str): El nombre del autor.

        Returns:
            List[Autor]: La lista de autores encontrados.

        Raises:
            AutorNoEncontrado: Si no se encuentran autores con el nombre dado.
        """
        autores = self.repo.buscar_por_nombre(nombre)
        if not autores:
            raise AutorNoEncontrado()
        return autores

    def obtener_todos(self) -> List[Autor]:
        """
        Obtiene todos los autores.

        Returns:
            List[Autor]: La lista de autores.
        """
        return self.repo.listar_todos()
    
    def editar_metadata_autor(self, autor_id: UUID, metadatos: Dict) -> Optional[bool]:
        """
        Edita los metadatos de un autor.

        Args:
            autor_id (UUID): El ID del autor.
            metadatos (dict): Los metadatos a editar.

        Returns:
            Optional[bool]: True si la edición se realizó correctamente, False en caso contrario.
        """
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
    
    def eliminar(self, autor_id: UUID) -> None:
        """
        Elimina un autor por su ID.

        Args:
            autor_id (UUID): El ID del autor.
        """
        self.repo.eliminar(autor_id)