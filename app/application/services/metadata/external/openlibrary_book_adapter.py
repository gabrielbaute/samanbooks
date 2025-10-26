import requests
import logging
from typing import Dict, List, Optional

from app.application.services.metadata.external.book_metadata_provider import BookMetadataProvider

class OpenLibraryBookAdapter(BookMetadataProvider):
    BASE_URL = "https://openlibrary.org"
    logger = logging.getLogger(__name__)

    def search_by_isbn(self, isbn: str) -> Optional[Dict]:
        url = f"{self.BASE_URL}/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.warning(f"Error al buscar libro por ISBN '{isbn}': {response.status_code}")
            return None

        data = response.json()
        book_data = data.get(f"ISBN:{isbn}")
        if not book_data:
            return None

        return {
            "titulo": book_data.get("title"),
            "autores": [a.get("name") for a in book_data.get("authors", [])],
            "editorial": book_data.get("publishers", [{}])[0].get("name"),
            "year": book_data.get("publish_date"),
            "descripcion": book_data.get("notes"),
            "isbn": isbn,
            "portada_url": book_data.get("cover", {}).get("large")
        }

    def search_by_title(self, title: str) -> Optional[Dict]:
        url = f"{self.BASE_URL}/search.json?title={title}"
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.warning(f"Error al buscar libro por título '{title}': {response.status_code}")
            return None

        docs = response.json().get("docs", [])
        if not docs:
            return None

        doc = docs[0]  # Tomamos el más relevante
        return {
            "titulo": doc.get("title"),
            "autores": doc.get("author_name", []),
            "year": str(doc.get("first_publish_year")) if doc.get("first_publish_year") else None,
            "isbn": doc.get("isbn", [None])[0],
            "portada_url": f"https://covers.openlibrary.org/b/id/{doc.get('cover_i')}-L.jpg" if doc.get("cover_i") else None
        }

    def search_by_author(self, author_name: str) -> List[Dict]:
        url = f"{self.BASE_URL}/search.json?author={author_name}"
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.warning(f"Error al buscar libros por autor '{author_name}': {response.status_code}")
            return []

        return response.json().get("docs", [])

    def search_by_query(self, query: str) -> List[Dict]:
        url = f"{self.BASE_URL}/search.json?q={query}"
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.warning(f"Error en búsqueda libre '{query}': {response.status_code}")
            return []

        return response.json().get("docs", [])

    def get_work_details(self, work_key: str) -> Dict:
        url = f"{self.BASE_URL}/works/{work_key}.json"
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.warning(f"Error al obtener detalles de obra '{work_key}': {response.status_code}")
            return {}

        return response.json()

    def get_edition_details(self, edition_key: str) -> Dict:
        url = f"{self.BASE_URL}/books/{edition_key}.json"
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.warning(f"Error al obtener detalles de edición '{edition_key}': {response.status_code}")
            return {}

        return response.json()
