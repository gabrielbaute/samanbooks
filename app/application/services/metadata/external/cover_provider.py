from abc import ABC, abstractmethod
from typing import Optional

class CoverProvider(ABC):
    @abstractmethod
    def get_cover_by_isbn(self, isbn: str, size: str = "L") -> Optional[str]:
        """
        Devuelve la URL de la portada basada en el ISBN.

        Args:
            isbn: Código ISBN del libro.
            size: Tamaño de la imagen ('S', 'M', 'L').

        Returns:
            URL de la imagen o None si no se encuentra.
        """
        pass

    @abstractmethod
    def get_cover_by_olid(self, olid: str, size: str = "L") -> Optional[str]:
        """
        Devuelve la URL de la portada basada en el Open Library ID.

        Args:
            olid: Identificador OLID del libro.
            size: Tamaño de la imagen ('S', 'M', 'L').

        Returns:
            URL de la imagen o None si no se encuentra.
        """
        pass
