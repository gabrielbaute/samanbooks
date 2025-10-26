import requests
import logging
from typing import Dict, List

from app.application.services.metadata.external.author_metadata_provider import AuthorMetadataProvider


class OpenLibraryAuthorAdapter(AuthorMetadataProvider):
    BASE_URL = "https://openlibrary.org"
    logger = logging.getLogger(__name__)

    def search_author(self, name: str) -> List[Dict]:
        url = f"{self.BASE_URL}/search/authors.json?q={name}"
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.warning(f"Error al buscar autor '{name}': {response.status_code}")
            return []

        data = response.json()
        return data.get("docs", [])

    def get_author_details(self, author_key: str) -> Dict:
        url = f"{self.BASE_URL}/authors/{author_key}.json"
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.warning(f"Error al obtener detalles de autor '{author_key}': {response.status_code}")
            return {}

        return response.json()

    def get_author_works(self, author_key: str, limit: int = 100) -> List[Dict]:
        url = f"{self.BASE_URL}/authors/{author_key}/works.json?limit={limit}"
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.warning(f"Error al obtener obras de autor '{author_key}': {response.status_code}")
            return []

        data = response.json()
        return data.get("entries", [])

    def get_work_details(self, work_key: str) -> Dict:
        url = f"{self.BASE_URL}/works/{work_key}.json"
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.warning(f"Error al obtener detalles de obra: {response.status_code}")
            return {}

        return response.json()  