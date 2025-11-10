from decimal import Decimal

from sqlalchemy.orm import DeclarativeBase,  mapped_column
from sqlalchemy import select
from app.models import Wallet
from app.exceptions import InsufficientFundsError, UserNotFoundError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.shemas import WalletResponse


class PostgreSQL():

    def __init__(self,DATABASE_URL):
        self.engine = create_async_engine(DATABASE_URL)
        self.SessionLocal = async_sessionmaker(self.engine,class_=AsyncSession,expire_on_commit=False)

    async def operation(self,UUID:str,operation_type:str,amount:Decimal):

        async  with self.SessionLocal() as session:
            try:
                async with session.begin():

                    wallet = (await session.scalars(select(Wallet).where(Wallet.id == UUID).with_for_update())).first()

                    if wallet is None:
                        raise UserNotFoundError(f"Пользователь {UUID} не найден")
                    # ОБНОВЛЯЕМ ДАННЫЕ ИЗ БД
                    await session.refresh(wallet)

                    print(f"Wallet: {wallet}")
                    print(f"Wallet ID: {wallet.id}")
                    print(f"Wallet balance: {wallet.balance}")  # Теперь покажет 1000

                    if operation_type == "DEPOSIT":
                        wallet.balance += amount
                        print(f"{wallet.balance=}")

                    elif operation_type == "WITHDRAW":
                        if wallet.balance < amount:
                            raise InsufficientFundsError("На балансе недостаточно средств")
                        wallet.balance -= amount
                    else:
                        raise ValueError(f"Неизвестный тип операции: {operation_type}")
                return (operation_type, amount)
            except Exception:
                # session.rollback()
                raise



    async def get_wallet_balance(self,UUID:str):

        async with self.SessionLocal() as session:
            result = await session.scalars(select(Wallet).where(Wallet.id ==UUID))
            user = result.first()
            if user is None:
                raise UserNotFoundError(f"Пользователь {UUID} не найден")
            return user.balance