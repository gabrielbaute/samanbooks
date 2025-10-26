from abc import ABC, abstractmethod
from typing import Dict, List

class AuthorMetadataProvider(ABC):
    @abstractmethod
    def search_author(self, name: str) -> List[Dict]:
        """
        Busca autores por nombre.

        Returns:
            Lista de resultados con claves como 'key', 'name', 'birth_date', etc.
        """
        pass

    @abstractmethod
    def get_author_details(self, author_key: str) -> Dict:
        """
        Obtiene detalles completos de un autor por su clave Open Library.

        Returns:
            Diccionario con nombre, fecha de nacimiento, biografía, etc.
        """
        pass

    @abstractmethod
    def get_author_works(self, author_key: str, limit: int = 100) -> List[Dict]:
        """
        Obtiene obras publicadas por el autor.

        Returns:
            Lista de obras con título, fecha, identificador, etc.
        """
        pass

    @abstractmethod
    def get_work_details(self, work_key: str) -> Dict:
        """
        Obtiene detalles completos de una obra por su clave Open Library.

        Args:
            work_key (str): Clave de la obra en Open Library.
        
        Returns:
            Diccionario con los detalles de la obra.
        """
        pass