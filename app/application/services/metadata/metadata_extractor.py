from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict

class MetadataExtractor(ABC):
    @abstractmethod
    def extract_metadata(self, path: Path) -> Dict:
        """Extrae metadatos desde un archivo de libro."""
        pass
