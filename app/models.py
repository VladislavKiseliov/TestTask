from decimal import Decimal
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import NUMERIC
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid

class Base(DeclarativeBase):
    pass

class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    balance: Mapped[Decimal] = mapped_column(
        NUMERIC(precision=10, scale=2),  # тип с параметрами
        nullable=False,
        default=Decimal('0.00')  # правильный default для Decimal
    )