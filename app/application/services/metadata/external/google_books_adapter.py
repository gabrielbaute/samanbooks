import requests
import logging
from typing import Dict, List, Optional

from app.application.services.metadata.external.book_metadata_provider import BookMetadataProvider

class GoogleBooksAdapter(BookMetadataProvider):
    BASE_URL = "https://www.googleapis.com/books/v1"
    logger = logging.getLogger(__name__)

    def search_by_isbn(self, isbn: str) -> Optional[Dict]:
        return self._search(f"isbn:{isbn}")

    def search_by_title(self, title: str) -> Optional[Dict]:
        return self._search(f"intitle:{title}")

    def search_by_author(self, author_name: str) -> List[Dict]:
        return self._search_raw(f"inauthor:{author_name}")

    def search_by_query(self, query: str) -> List[Dict]:
        return self._search_raw(query)

    def get_work_details(self, work_key: str) -> Dict:
        url = f"{self.BASE_URL}/volumes/{work_key}"
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.warning(f"Error al obtener detalles de volumen '{work_key}': {response.status_code}")
            return {}
        return response.json()

    def get_edition_details(self, edition_key: str) -> Dict:
        return self.get_work_details(edition_key)

    def _search(self, query: str) -> Optional[Dict]:
        results = self._search_raw(query)
        return results[0] if results else None

    def _search_raw(self, query: str) -> List[Dict]:
        url = f"{self.BASE_URL}/volumes?q={query}"
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.warning(f"Error en búsqueda Google Books '{query}': {response.status_code}")
            return []

        items = response.json().get("items", [])
        libros = []
        for item in items:
            info = item.get("volumeInfo", {})
            libros.append({
                "titulo": info.get("title"),
                "autores": info.get("authors", []),
                "editorial": info.get("publisher"),
                "year": info.get("publishedDate", "")[:4],
                "descripcion": info.get("description"),
                "isbn": self._extract_isbn(info),
                "portada_url": info.get("imageLinks", {}).get("thumbnail")
            })
        return libros

    def _extract_isbn(self, info: Dict) -> Optional[str]:
        for iden in info.get("industryIdentifiers", []):
            if iden.get("type") in {"ISBN_13", "ISBN_10"}:
                return iden.get("identifier")
        return None
