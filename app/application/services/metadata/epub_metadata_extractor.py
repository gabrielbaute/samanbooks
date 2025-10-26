import logging
import ebooklib
from pathlib import Path
from ebooklib import epub
from typing import Dict, Optional

from app.application.services.metadata.metadata_extractor import MetadataExtractor

class EpubMetadataExtractor(MetadataExtractor):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def extract_metadata(self, path: Path) -> Dict:
        """
        Extrae metadatos de un archivo EPUB.

        Args:
            path (Path): Ruta al archivo EPUB.

        Returns:
            Dict: Diccionario con los metadatos extraídos.
        """
        book = epub.read_epub(str(path))
        metadata = {
            "titulo": None,
            "autores": [],
            "editorial": None,
            "year": None,
            "descripcion": None,
            "isbn": None,
            "paginas": None,
            "portada_bytes": None,
            "formato": "epub",
            "portada_hash": None
        }

        if 'DC:title' in book.metadata:
            metadata['titulo'] = book.metadata['DC:title'][0][0]

        if 'DC:creator' in book.metadata:
            metadata['autores'] = [creator[0] for creator in book.metadata['DC:creator']]

        if 'DC:publisher' in book.metadata:
            metadata['editorial'] = book.metadata['DC:publisher'][0][0]

        if 'DC:date' in book.metadata:
            metadata['year'] = book.metadata['DC:date'][0][0][:4]

        if 'DC:description' in book.metadata:
            metadata['descripcion'] = book.metadata['DC:description'][0][0]

        if 'DC:identifier' in book.metadata:
            for identifier in book.metadata['DC:identifier']:
                if 'isbn' in identifier[1].get('scheme', '').lower():
                    metadata['isbn'] = identifier[0]
                    break

        portada = self._get_cover(book)
        if portada:
            metadata['portada_bytes'] = portada
            metadata['portada_hash'] = self._hash_bytes(portada)

        self.logger.debug(f"Metadatos EPUB extraídos de {path.name}: {metadata}")
        return metadata

    def _get_cover(self, book: epub.EpubBook) -> Optional[bytes]:
        """
        Obtiene la imagen de portada de un libro EPUB.

        Args:
            book (epub.EpubBook): Objeto EPUB del libro.

        Returns:
            Optional[bytes]: Datos de la imagen de portada, o None si no hay portada.
        """
        cover_item = book.get_item_with_id('cover')
        if cover_item:
            return cover_item.content

        for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
            if 'cover' in item.get_name().lower():
                return item.content
        return None

    def _hash_bytes(self, data: bytes) -> str:
        """
        Calcula el hash SHA-256 de los datos.
        
        Args:
            data (bytes): Datos a hashear.

        Returns:
            str: Hash SHA-256 en formato hexadecimal.
        """
        import hashlib
        return hashlib.sha256(data).hexdigest()
