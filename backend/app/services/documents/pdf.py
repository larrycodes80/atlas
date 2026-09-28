import fitz

def extract_text(file_path: str) -> list[dict]:
    document = fitz.open(file_path)

    pages = []


    for page_number, page in enumerate(document, 1):
        pages.append(
            {
                "page_number":page_number,
                "text": page.get_text()
            }
        )

    document.close()

    return pages
