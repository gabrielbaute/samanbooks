from pathlib import Path
from typing import Dict, Optional
from PyPDF2 import PdfReader
import logging

from app.application.services.metadata.metadata_extractor import MetadataExtractor

class PdfMetadataExtractor(MetadataExtractor):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def extract_metadata(self, file_path: Path) -> Dict[str, Optional[str]]:
        """
        Extrae metadatos básicos desde un archivo PDF.

        Returns:
            Dict con claves como 'titulo', 'autores', 'year', 'num_paginas'
        """
        metadata = {
            "titulo": None,
            "autores": [],
            "year": None,
            "num_paginas": None
        }

        try:
            reader = PdfReader(str(file_path))
            doc_info = reader.metadata
            metadata["titulo"] = doc_info.title
            if doc_info.author:
                metadata["autores"] = [doc_info.author]
            metadata["year"] = self._extract_year(doc_info)
            metadata["num_paginas"] = str(len(reader.pages))
        except Exception as e:
            self.logger.warning(f"Error al extraer metadatos de PDF: {e}")

        return metadata

    def _extract_year(self, doc_info) -> Optional[str]:
        # Intenta extraer el año desde la fecha de creación
        date_str = getattr(doc_info, "creation_date", None)
        if date_str and len(date_str) >= 6:
            # Formato típico: D:YYYYMMDD...
            return date_str[2:6]
        return None