import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    id: Mapped[UUID] = mapped_column(
        UUID,
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
    )


class CreatedUpdatedMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
