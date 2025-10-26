from flask_jwt_extended import JWTManager
from flask import Flask


def load_jwt_manager(application: Flask) -> None:
    """Función que inicializa la extensión JWTManager.
    
    Args:
        application (Flask): La aplicación Flask.
    """
    jwt = JWTManager(application)
    return jwt