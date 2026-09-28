from pydantic import BaseModel, Field

class TableContent(BaseModel):
    page_number: int
    rows: list[list[str]] = Field(default_factory=list)

class ImageContent(BaseModel):
    page_number: int
    image_index: int
    width: int
    height: int
    path: str | None = None


class PageContent(BaseModel):
    page_number: int
    text: str = ""
    tables: list[TableContent] = Field(default_factory=list)
    images: list[ImageContent] = Field(default_factory=list)


class DocumentContent(BaseModel):
    filename: str
    page_count: int
    pages: list[PageContent]