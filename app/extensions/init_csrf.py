from flask import Flask, Blueprint
from flask_wtf import CSRFProtect

def init_csrf(application: Flask, api_bp: Blueprint) -> None:
    """Función que inicializa la extensión CSRFProtect.
    
    Args:
        application (Flask): La aplicación Flask.
        api_bp (Blueprint): El blueprint de la API.
    """

    csrf = CSRFProtect()

    application.config['WTF_CSRF_ENABLED'] = True
    csrf.init_app(application)
    csrf.exempt(api_bp)
    return csrf
