from flask import Flask
from datetime import datetime

from app.config import AppConfig
from app.extensions import init_csrf, init_login_manager, load_jwt_manager, init_migrate
from app.frontend.routes import register_routes
from app.infrastructure.database.db_config import init_db, db
from app.infrastructure.database.repositories import (
    SQLAlchemyLibroRepository,
    SQLAlchemyAutorRepository,
    SQLAlchemySerieRepository,
    SQLAlchemyMarcadorRepository,
    SQLAlchemyProgresoRepository,
    SQLAlchemyUsuarioRepository
)
from app.infrastructure.services import (
    LibroServiceImpl,
    AutorServiceImpl,
    SerieServiceImpl,
    MarcadorServiceImpl,
    ProgresoServiceImpl,
    UsuarioServiceImpl
)
from app.application.services.metadata import (
    FolderMetadataBuilder,
    EpubMetadataExtractor,
    PdfMetadataExtractor,
    OpenLibraryBookAdapter,
    OpenLibraryAuthorAdapter,
    OpenLibraryCoverAdapter,
    GoogleBooksAdapter,
)
from app.application.services import ScannerService

def create_app():
    application = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )
    application.config.from_object(AppConfig)

    # Inicializar extensiones
    init_db(application)
    load_jwt_manager(application)
    init_login_manager(application)
    init_migrate(application, db)

    # Repositorios
    libro_repo = SQLAlchemyLibroRepository()
    autor_repo = SQLAlchemyAutorRepository()
    serie_repo = SQLAlchemySerieRepository()
    marcador_repo = SQLAlchemyMarcadorRepository()
    progreso_repo = SQLAlchemyProgresoRepository()
    usuario_repo = SQLAlchemyUsuarioRepository()

    # Servicios
    libro_service = LibroServiceImpl(libro_repo)
    autor_service = AutorServiceImpl(autor_repo)
    serie_service = SerieServiceImpl(serie_repo)
    marcador_service = MarcadorServiceImpl(marcador_repo)
    progreso_service = ProgresoServiceImpl(progreso_repo)
    usuario_service = UsuarioServiceImpl(usuario_repo)
    folder_builder = FolderMetadataBuilder()
    epub_extractor = EpubMetadataExtractor()
    pdf_extractor = PdfMetadataExtractor()
    book_providers = [
        OpenLibraryBookAdapter(),
        GoogleBooksAdapter()
    ]
    author_provider = OpenLibraryAuthorAdapter()
    cover_provider = OpenLibraryCoverAdapter()

    # Scanner
    scanner = ScannerService(
        folder_builder=folder_builder,
        epub_extractor=epub_extractor,
        pdf_extractor=pdf_extractor,
        book_providers=book_providers,
        author_provider=author_provider,
        cover_provider=cover_provider,
        libro_service=libro_service,
        autor_service=autor_service,
        serie_service=serie_service
    )

    # Registrar rutas
    register_routes(application, scanner)

    with application.app_context():
        db.create_all()

    @application.context_processor
    def inject_app_variables():
        return {
            "app_name": application.config["APP_NAME"],
            "app_version": application.config["APP_VERSION"],
            "now": datetime.now()
            }

    return application
