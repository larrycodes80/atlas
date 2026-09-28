from abc import ABC, abstractmethod
from pathlib import Path

from app.schemas.extraction import DocumentContent



class DocumentExtractor(ABC):

    @abstractmethod
    def extract(self, file_path: Path) -> DocumentContent:
        """Extract all information from PDF and return structured content."""
        raise NotImplementedError


    