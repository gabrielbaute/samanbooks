from uuid import uuid4, UUID
from typing import Optional, List, Dict
from datetime import date

from app.domain.services import UsuarioService
from app.domain.entities import Usuario
from app.domain.enums import Rol
from app.domain.exceptions import MetadatosIncompletos, UsuarioInvalido, UsuarioNoEncontrado
from app.infrastructure.database.repositories.sqlalchemy_usuario_repository import SQLAlchemyUsuarioRepository

class UsuarioServiceImpl(UsuarioService):
    def __init__(self, usuario_repo: SQLAlchemyUsuarioRepository):
        self.repo = usuario_repo

    def registrar_usuario(self, username, password_hash, email, rol = Rol.LECTOR) -> Usuario:
        if not username or not password_hash or not email:
            raise MetadatosIncompletos()

        usuario = Usuario(
            id=uuid4(),
            username=username,
            password_hash=password_hash,
            email=email,
            rol=rol,
            fecha_registro=date.today()
        )

        try:
            self.repo.guardar(usuario)
        except Exception as e:
            raise UsuarioInvalido(f"Error al crear el usuario: {e}")

        return usuario
    
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        usuario = self.repo.obtener_por_email(email)
        if not usuario:
            raise UsuarioNoEncontrado()
        return usuario
    
    def obtener_por_id(self, usuario_id: str) -> Optional[Usuario]:
        usuario = self.repo.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado()
        return usuario
    
    def obtener_todos(self) -> List[Usuario]:
        return self.repo.listar_todos()
    
    def eliminar(self, usuario_id: str) -> None:
        self.repo.eliminar(usuario_id)
    
    def cambiar_rol(self, usuario_id: str, nuevo_rol: str) -> Optional[bool]:
        usuario = self.repo.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado()
        try:
            usuario.rol = nuevo_rol
            self.repo.guardar(usuario)
            return True
        except Exception as e:
            return False
    
    def cambiar_password(self, usuario_id: str, nueva_password: str) -> Optional[bool]:
        usuario = self.repo.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado()
        try:
            usuario.password_hash = nueva_password
            self.repo.guardar(usuario)
        except Exception as e:
            raise

    def cambiar_email(self, usuario_id, nuevo_email) -> Optional[bool]:
        usuario = self.repo.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado()
        try:
            usuario.email = nuevo_email
            self.repo.guardar(usuario)
        except Exception as e:
            raise
    
    def cambiar_username(self, usuario_id, nuevo_username) -> Optional[bool]:
        usuario = self.repo.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado()
        try:
            usuario.username = nuevo_username
            self.repo.guardar(usuario)
        except Exception as e:
            raise