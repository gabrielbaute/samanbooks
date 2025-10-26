from pathlib import Path
from typing import List, Dict
import logging
import hashlib

from app.domain.enums import Formato
from app.domain.services import (
    LibroService, 
    AutorService, 
    SerieService
)
from app.application.services.metadata import (
    FolderMetadataBuilder,
    EpubMetadataExtractor,
    PdfMetadataExtractor,
    BookMetadataProvider,
    AuthorMetadataProvider,
    CoverProvider,
)

class ScannerService:
    def __init__(
        self,
        folder_builder: FolderMetadataBuilder,
        epub_extractor: EpubMetadataExtractor,
        pdf_extractor: PdfMetadataExtractor,
        book_providers: List[BookMetadataProvider],
        author_provider: AuthorMetadataProvider,
        cover_provider: CoverProvider,
        libro_service: LibroService,
        autor_service: AutorService,
        serie_service: SerieService,
    ):
        self.logger = logging.getLogger(f"[{self.__class__.__name__}]")
        self.folder_builder = folder_builder
        self.epub_extractor = epub_extractor
        self.pdf_extractor = pdf_extractor
        self.book_providers = book_providers
        self.author_provider = author_provider
        self.cover_provider = cover_provider
        self.libro_service = libro_service
        self.autor_service = autor_service
        self.serie_service = serie_service

    def _determinar_formato(self, file_path: Path):
        ext = file_path.suffix.lower()
        if ext == ".epub":
            return Formato.EPUB
        elif ext == ".pdf":
            return Formato.PDF
        return Formato.DESCONOCIDO

    def _extract_content_metadata(self, file_path: Path) -> Dict:
        if file_path.suffix.lower() == ".epub":
            return self.epub_extractor.extract_metadata(file_path)
        elif file_path.suffix.lower() == ".pdf":
            return self.pdf_extractor.extract_metadata(file_path)
        return {}

    def _enrich_metadata(self, metadata: Dict) -> Dict:
        isbn = metadata.get("isbn")
        enriched = {}

        for provider in self.book_providers:
            if isbn:
                enriched = provider.search_by_isbn(isbn)
            if not enriched and metadata.get("titulo"):
                enriched = provider.search_by_title(metadata["titulo"])
            if enriched:
                break

        portada_url = None
        if isbn:
            portada_url = self.cover_provider.get_cover_by_isbn(isbn)
        elif enriched.get("portada_url"):
            portada_url = enriched["portada_url"]

        return {**metadata, **(enriched or {}), "portada_url": portada_url}

    def _generar_hash_portada(self, portada_url: str) -> str:
        if not portada_url:
            return "sin_portada"
        return hashlib.md5(portada_url.encode("utf-8")).hexdigest()

    def _registrar_libro(self, file_path: Path, metadata: Dict):
        try:
            titulo = metadata.get("titulo")
            autores_nombres = metadata.get("autores", [])
            serie_nombre = metadata.get("serie")
            isbn = metadata.get("isbn")
            year = metadata.get("year")
            descripcion = metadata.get("descripcion")
            editorial = metadata.get("editorial")
            fecha_publicacion = metadata.get("fecha_publicacion")
            paginas = metadata.get("paginas")
            portada_url = metadata.get("portada_url")
            formato = self._determinar_formato(file_path)
            portada_hash = self._generar_hash_portada(portada_url)

            # 1. Registrar autores
            autores_ids = []
            for nombre in autores_nombres:
                autor = self.autor_service.buscar_o_crear_por_nombre(nombre)
                autores_ids.append(autor.id)

            # 2. Registrar serie si aplica
            serie_id = None
            if serie_nombre:
                serie = self.serie_service.buscar_o_crear_por_nombre(serie_nombre)
                serie_id = serie.id

            # 3. Registrar libro
            self.libro_service.registrar_libro(
                titulo=titulo,
                autores=autores_ids,
                path=str(file_path),
                formato=formato,
                portada_hash=portada_hash,
                isbn=isbn,
                fecha_publicacion=fecha_publicacion,
                editorial=editorial,
                serie_id=serie_id,
                descripcion=descripcion,
                paginas=paginas,
                year=year
            )

            self.logger.info(f"✅ Libro registrado: {titulo}")
        except Exception as e:
            self.logger.warning(f"❌ Error al registrar libro '{file_path.name}': {e}")


    def escanear_directorio(self, base_path: Path):
        for file_path in base_path.rglob("*"):
            if file_path.suffix.lower() not in {".epub", ".pdf"}:
                continue

            self.logger.info(f"📘 Escaneando: {file_path.name}")

            # 1. Extraer metadatos locales
            folder_meta = self.folder_builder.build_metadata(file_path)
            content_meta = self._extract_content_metadata(file_path)

            # 2. Combinar y enriquecer
            metadata = {**folder_meta, **content_meta}
            enriched = self._enrich_metadata(metadata)

            # 3. Registrar entidades
            self._registrar_libro(file_path, enriched)
