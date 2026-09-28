from pathlib import Path

import fitz
from PIL import Image

from app.schemas.extraction import (
    DocumentContent,
    ImageContent,
    PageContent,
)
from app.services.extraction.base import DocumentExtractor
from app.services.extraction.ocr import TesseractOCRExtractor


class PyMuPDFExtractor(DocumentExtractor):

    def __init__(self) -> None:
        self.ocr_extractor = TesseractOCRExtractor()

    def extract(self, file_path: Path) -> DocumentContent:
        """
        Extract text and embedded image metadata from a PDF.

        Text-based pages use PyMuPDF text extraction.

        Pages with little/no extractable text are rendered and
        passed through Tesseract OCR.
        """

        pages: list[PageContent] = []

        with fitz.open(file_path) as document:

            for page_number, page in enumerate(document, start=1):

                text = page.get_text("text").strip()

                images: list[ImageContent] = []

                # Detect embedded images.
                embedded_images = page.get_images(full=True)

                for image_index, image_info in enumerate(
                    embedded_images,
                    start=1,
                ):
                    xref = image_info[0]

                    image_data = document.extract_image(xref)

                    width = image_data["width"]
                    height = image_data["height"]

                    images.append(
                        ImageContent(
                            page_number=page_number,
                            image_index=image_index,
                            width=width,
                            height=height,
                        )
                    )

                # If the page contains little/no text, treat it as
                # potentially scanned and run OCR.
                if not text:
                    text = self._ocr_page(page)

                pages.append(
                    PageContent(
                        page_number=page_number,
                        text=text,
                        images=images,
                    )
                )

            return DocumentContent(
                filename=file_path.name,
                page_count=len(document),
                pages=pages,
            )

    def _ocr_page(self, page: fitz.Page) -> str:
        """
        Render a PDF page into an image and run Tesseract OCR.
        """

        matrix = fitz.Matrix(2, 2)

        pixmap = page.get_pixmap(
            matrix=matrix,
            alpha=False,
        )

        image = Image.frombytes(
            "RGB",
            [pixmap.width, pixmap.height],
            pixmap.samples,
        )

        return self.ocr_extractor.extract_image(image)