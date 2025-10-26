import logging
from typing import Optional

from app.application.services.metadata.external.cover_provider import CoverProvider

class OpenLibraryCoverAdapter(CoverProvider):
    BASE_URL = "https://covers.openlibrary.org"
    logger = logging.getLogger(__name__)

    def get_cover_by_isbn(self, isbn: str, size: str = "L") -> Optional[str]:
        if not isbn:
            return None
        url = f"{self.BASE_URL}/b/isbn/{isbn}-{size}.jpg"
        return url

    def get_cover_by_olid(self, olid: str, size: str = "L") -> Optional[str]:
        if not olid:
            return None
        url = f"{self.BASE_URL}/b/olid/{olid}-{size}.jpg"
        return url
