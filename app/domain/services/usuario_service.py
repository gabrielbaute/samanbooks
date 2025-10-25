from uuid import uuid4
from datetime import date
from typing import Optional, List

from domain.entities import Usuario
from domain.repositories import UsuarioRepository
from domain.exceptions import UsuarioNoEncontrado
from domain.enums import Rol

class UsuarioService:
    def __init__(self, usuario_repo: UsuarioRepository):
        self.repo = usuario_repo

    def registrar_usuario(self, username: str, password_hash: str, email: str, rol: Rol = Rol.LECTOR) -> Usuario:
        """
        Registra un nuevo usuario.
        
        Args:
            username (str): El nombre de usuario del usuario.
            password_hash (str): El hash de la contraseña del usuario.
            email (str): El email del usuario.
            rol (Rol): El rol del usuario.
        
        Returns:
            Usuario: El usuario registrado.
        """
        usuario = Usuario(
            id=uuid4(),
            username=username,
            password_hash=password_hash,
            email=email,
            rol=rol,
            fecha_registro=date.today()
        )
        self.repo.guardar(usuario)
        return usuario

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su email.
        
        Args:
            email (str): El email del usuario.
        
        Returns:
            Usuario: El usuario encontrado, o None si no se encuentra.
        """
        usuario = self.repo.obtener_por_email(email)
        if not usuario:
            raise UsuarioNoEncontrado()
        return usuario

    def obtener_por_id(self, usuario_id: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su ID.
        
        Args:
            usuario_id (str): El ID del usuario.
        
        Returns:
            Usuario: El usuario encontrado, o None si no se encuentra.
        """
        usuario = self.repo.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado()
        return usuario
    
    def obtener_todos(self) -> List[Usuario]:
        """
        Obtiene todos los usuarios.
        
        Returns:
            List[Usuario]: La lista de usuarios.
        """
        return self.repo.listar_todos()
    
    def eliminar(self, usuario_id: str) -> None:
        """
        Elimina un usuario por su ID.
        
        Args:
            usuario_id (str): El ID del usuario.
        """
        self.repo.eliminar(usuario_id)
    
    def cambiar_rol(self, usuario_id: str, nuevo_rol: str) -> Optional[bool]:
        """
        Cambia el rol de un usuario.

        Args:
            usuario_id (str): El ID del usuario.
            nuevo_rol (str): El nuevo rol del usuario.

        Returns:
            bool: True si el rol se cambió correctamente, False en caso contrario.
        """
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
        """
        Cambia la contraseña de un usuario.

        Args:
            usuario_id (str): El ID del usuario.
            nueva_password (str): La nueva contraseña del usuario.

        Returns:
            bool: True si la contraseña se cambió correctamente, False en caso contrario.
        """
        usuario = self.repo.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado()
        try:
            usuario.password_hash = nueva_password
            self.repo.guardar(usuario)
        except Exception as e:
            raise
    
    def cambiar_email(self, usuario_id: str, nuevo_email: str) -> Optional[bool]:
        """
        Cambia el email de un usuario.

        Args:
            usuario_id (str): El ID del usuario.
            nuevo_email (str): El nuevo email del usuario.

        Returns:
            bool: True si el email se cambió correctamente, False en caso contrario.
        """
        usuario = self.repo.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado()
        try:
            usuario.email = nuevo_email
            self.repo.guardar(usuario)
        except Exception as e:
            raise
    
    def cambiar_username(self, usuario_id: str, nuevo_username: str) -> Optional[bool]:
        """
        Cambia el username de un usuario.

        Args:
            usuario_id (str): El ID del usuario.
            nuevo_username (str): El nuevo username del usuario.

        Returns:
            bool: True si el username se cambió correctamente, False en caso contrario.
        """
        usuario = self.repo.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado()
        try:
            usuario.username = nuevo_username
            self.repo.guardar(usuario)
        except Exception as e:
            raise