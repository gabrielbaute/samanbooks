from typing import List, Optional
from datetime import datetime
from uuid import UUID

from domain.entities.usuario import Usuario
from domain.repositories.usuario_repository import UsuarioRepository
from infrastructure.database.models.usuario_model import UsuarioModel


class SQLAlchemyUsuarioRepository(UsuarioRepository):
    def __init__(self, session):
        self.session = session

    def guardar(self, usuario: Usuario) -> None:
        """
        Guarda un usuario en la base de datos.

        Args:
            usuario (Usuario): El usuario a guardar.
        """
        modelo = UsuarioModel(
            id=usuario.id,
            username=usuario.username,
            password_hash=usuario.password_hash,
            email=usuario.email,
            rol=usuario.rol,
            fecha_registro=usuario.fecha_registro
        )
        self.session.add(modelo)
        self.session.commit()

    def obtener_por_id(self, id: UUID) -> Optional[Usuario]:
        """
        Obtiene un usuario por su ID.

        Args:
            id (UUID): El ID del usuario.

        Returns:
            Optional[Usuario]: El usuario encontrado o None si no se encuentra.
        """
        modelo = self.session.get(UsuarioModel, id)
        return Usuario(**modelo.__dict__) if modelo else None

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su email.

        Args:
            email (str): El email del usuario.
        
        Returns:
            Optional[Usuario]: El usuario encontrado o None si no se encuentra.
        """
        if not email:
            return None
        modelo = self.session.query(UsuarioModel).filter_by(email=email).first()
        return Usuario(**modelo.__dict__) if modelo else None

    def obtener_todos(self) -> List[Usuario]:
        """
        Obtiene una lista de todos los usuarios.

        Returns:
            List[Usuario]: Una lista de todos los usuarios.
        """
        modelos = self.session.query(UsuarioModel).all()
        return [Usuario(**modelo.__dict__) for modelo in modelos]

    def eliminar(self, id: UUID) -> None:
        """
        Elimina un usuario por su ID.

        Args:
            id (UUID): El ID del usuario.
        """
        modelo = self.session.get(UsuarioModel, id)
        if modelo:
            self.session.delete(modelo)
            self.session.commit()