from flask_login import LoginManager
from flask import Flask

def init_login_manager(application: Flask):
    """Función que inicializa la extensión LoginManager.
    
    Args:
        application (Flask): La aplicación Flask.
    """

    login_manager = LoginManager()

    login_manager.init_app(application)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, inicie sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'

    return login_manager