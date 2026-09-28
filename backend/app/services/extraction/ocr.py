from pathlib import Path

from PIL import Image
import pytesseract

from app.schemas.extraction import (
    DocumentContent,
    ImageContent,
    PageContent,
)
from app.services.extraction.base import DocumentExtractor


class TesseractOCRExtractor(DocumentExtractor):

    SUPPORTED_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".tiff",
        ".bmp",
        ".webp",
    }

    def extract_image(self, image: Image.Image) -> str:
        """
        Run OCR on an already-loaded image.
        """

        rgb_image = image.convert("RGB")

        return pytesseract.image_to_string(rgb_image).strip()

    def extract(self, file_path: Path) -> DocumentContent:
        """
        Extract text from a standalone image file.
        """

        extension = file_path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported image format '{extension}'. "
                f"Supported formats: "
                f"{', '.join(sorted(self.SUPPORTED_EXTENSIONS))}"
            )

        with Image.open(file_path) as image:
            width, height = image.size

            text = self.extract_image(image)

            image_content = ImageContent(
                page_number=1,
                image_index=1,
                width=width,
                height=height,
                path=str(file_path),
            )

            page = PageContent(
                page_number=1,
                text=text,
                images=[image_content],
            )

            return DocumentContent(
                filename=file_path.name,
                page_count=1,
                pages=[page],
            )