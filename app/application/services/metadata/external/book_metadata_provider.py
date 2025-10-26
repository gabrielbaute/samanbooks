from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class BookMetadataProvider(ABC):
    @abstractmethod
    def search_by_isbn(self, isbn: str) -> Optional[Dict]: ...

    @abstractmethod
    def search_by_title(self, title: str) -> Optional[Dict]: ...

    @abstractmethod
    def search_by_author(self, author_name: str) -> List[Dict]: ...

    @abstractmethod
    def search_by_query(self, query: str) -> List[Dict]: ...

    @abstractmethod
    def get_work_details(self, work_key: str) -> Dict: ...

    @abstractmethod
    def get_edition_details(self, edition_key: str) -> Dict: ...
