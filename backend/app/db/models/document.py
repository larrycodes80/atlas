from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Datetime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Document(Base):
    __table__name = "documents"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )

    filename: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))
    mime_type: Mapped[str] = mapped_column(String(100))

    status: Mapped[str] = mapped_column(String(50), default="uploaded")

    created_at : Mapped[datetime] = mapped_column(Datetime, default=datetime.utcnow()) 