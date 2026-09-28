from pathlib import Path

import fitz

from app.schemas.extraction import (
    DocumentContent,
    ImageContent,
    PageContent,
)

from app.services.extraction.base import DocumentExtractor


class PyMuPDFExtractor(DocumentExtractor):

    def extract(self, file_path: Path) -> DocumentContent:
        document = fitz.open(file_path)

        pages: list[PageContent] = []

        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            images: list[ImageContent] = []

            for image_index, image in enumerate(
                page.get_images(full=True),
                start=1,
            ):
                xref = image[0]

                extracted = document.extract_image(xref)

                images.append(
                    ImageContent(
                        page_number=page_number,
                        image_index=image_index,
                        width=extracted["width"],
                        height=extracted["height"],
                    )
                )

            pages.append(
                PageContent(
                    page_number=page_number,
                    text=text,
                    images=images,
                )
            )

        page_count = len(document)

        document.close()

        return DocumentContent(
            filename=file_path.name,
            page_count=page_count,
            pages=pages,
        )