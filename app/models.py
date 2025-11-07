from decimal import Decimal

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker
from sqlalchemy import ForeignKey, create_engine,NUMERIC
from sqlalchemy.dialects.postgresql import UUID
import uuid



class Base(DeclarativeBase):
    pass

class Wallet(Base):

    __tablename__ = "wallets"

    uuid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance: Mapped[Decimal] = mapped_column(NUMERIC,nullable=False,default=0)