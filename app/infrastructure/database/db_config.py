from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def init_db(application: Flask):
    """Inicializa la base de datos
    
    Args:
        app (Flask): Instancia de la aplicación Flask
    """
    db.init_app(application)