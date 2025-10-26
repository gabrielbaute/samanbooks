from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask



def init_migrate(application: Flask, db: SQLAlchemy):
    """Función que inicializa la extensión Migrate.
    
    Args:
        app (Flask): Instancia de la aplicación Flask.
        db (SQLAlchemy): Instancia de la base de datos SQLAlchemy.
    """
    migrate = Migrate()
    migrate.init_app(application, db)