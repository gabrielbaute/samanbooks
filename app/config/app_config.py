import os
from dotenv import load_dotenv
from datetime import timedelta
from typing import Dict

load_dotenv()

BASE_DIR=os.path.abspath(os.path.dirname(__file__))

# Función para convertir una cadena a un valor booleano
def str_to_bool(value):
    """Convierte una cadena a un valor booleano.
    
    Args:
        value (str): La cadena a convertir.
    
    Return:
        bool: El valor booleano correspondiente.
    """
    return value.lower() in ['true', '1', 'yes']

class AppConfig:
    """Configuración de la aplicación. Esta clase recolecta y almacena las variables de entorno."""
    
    # Flask server
    BASEDIR = BASE_DIR
    APP_NAME = os.getenv('APP_NAME', 'SamanBooks')
    APP_VERSION = "0.1.0"
    APP_URL = os.getenv('APP_URL', 'http://localhost:5001')
    PORT = os.environ.get("PORT")
    HOST = os.environ.get("HOST")
    DEBUG = os.environ.get("DEBUG")
    LANGUAGE = os.environ.get("LANGUAGE")
    SCHEDULER_API_ENABLED = os.environ.get("SCHEDULER_API_ENABLED") or True

    # Admin inicial
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

    # Encriptado
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_secreta_segura'
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    RESET_TOKEN_EXP_MINUTES = int(os.getenv('RESET_TOKEN_EXP_MINUTES', 25))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 30)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 30)))

    # Configuración de Flask-Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = str_to_bool(os.environ.get('MAIL_USE_TLS', 'False'))
    MAIL_USE_SSL = str_to_bool(os.environ.get('MAIL_USE_SSL', 'True'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = (os.environ.get('APP_NAME'), os.environ.get('MAIL_USERNAME'))
    MAIL_DEBUG = int(os.environ.get('MAIL_DEBUG', 0))

    # BDD (en caso de usar un servidor)
    DB_HOST = os.environ.get('DB_HOST')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')
    DB_PORT = os.environ.get('DB_PORT')

    # BDD SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def get_db_config(self) -> dict:
        """Retorna un diccionario con la configuración de la base de datos de CERCAPP.
        
        Return:
            dict: Diccionario con la configuración de la base de datos.
        """
        return {
            'host': self.DB_HOST,
            'user': self.DB_USER,
            'password': self.DB_PASSWORD,
            'database': self.DB_NAME
        }
    
    def get_maria_db_url(self) -> str:
        """Retorna la URL de conexión a la base de datos MariaDB.
        
        Return:
            str: URL de conexión a la base de datos MariaDB.
        """
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    def get_sqlite_url(self) -> str:
        """Retorna la URL de conexión a la base de datos SQLite.
        
        Return:
            str: URL de conexión a la base de datos SQLite.
        """
        return f"sqlite:///{os.path.join(self.BASEDIR, 'database.db')}"

    def get_postgresql_url(self) -> str:
        """Retorna la URL de conexión a la base de datos PostgreSQL.
        
        Return:
            str: URL de conexión a la base de datos PostgreSQL.
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"