from decimal import Decimal

from sqlalchemy.orm import DeclarativeBase,  mapped_column
from sqlalchemy import select
from app.models import Wallet
from exceptions import InsufficientFundsError, UserNotFoundError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class PostgreSQL():

    def __init__(self,DATABASE_URL):
        self.engine = create_async_engine(DATABASE_URL)
        self.SessionLocal = async_sessionmaker(self.engine,class_=AsyncSession,expire_on_commit=False)

    async def operation(self,UUID:str,operation_type:str,amount:Decimal):

        async  with self.SessionLocal() as session:
            try:
                async with session.begin():

                    wallet = await session.scalars(select(Wallet).where(Wallet.uuid == UUID)).first()

                    if wallet is None:
                        raise UserNotFoundError(f"Пользователь {UUID} не найден")

                    if operation_type == "DEPOSIT":
                        wallet.balance += amount

                    elif operation_type == "WITHDRAW":
                        if wallet.balance < amount:
                            raise InsufficientFundsError("На балансе недостаточно средств")
                        wallet.balance -= amount
                    else:
                        raise ValueError(f"Неизвестный тип операции: {operation_type}")
            except Exception:
                # session.rollback()
                raise

    async def get_wallet_balance(self,UUID:str):

        async with self.SessionLocal() as session:
            user = await session.scalars(select(Wallet).where(Wallet.uuid ==UUID)).first()
            if user is None:
                raise UserNotFoundError(f"Пользователь {UUID} не найден")
            return user.balance