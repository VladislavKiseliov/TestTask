from decimal import Decimal

from sqlalchemy.orm import DeclarativeBase, Mapped,  mapped_column,Session, sessionmaker
from sqlalchemy import String, Integer, ForeignKey ,  DateTime , create_engine,select
from app.models import Wallet
from exceptions import InsufficientFundsError, UserNotFoundError


class PostgreSQL():

    def __init__(self,DATABASE_URL):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def operation(self,UUID:str,operation_type:str,amount:Decimal):

        with self.SessionLocal() as session:
            try:
                with session.begin():

                    wallet = session.scalars(select(Wallet).where(Wallet.uuid == UUID).with_for_update()).first()

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

    def get_wallet_balance(self,UUID:str):

        with self.SessionLocal() as session:
            user = session.scalars(select(Wallet).where(Wallet.uuid ==UUID)).first()
            if user is None:
                raise UserNotFoundError(f"Пользователь {UUID} не найден")
            return user.balance