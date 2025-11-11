from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from uuid import UUID as UUID_Type
from app.exceptions import InsufficientFundsError,UserNotFoundError
from app.database import PostgreSQL
from app.shemas import WalletOperation, WalletResponse

app = FastAPI()
DATABASE_URL = os.getenv("DATABASE_URL")
database = PostgreSQL(DATABASE_URL)


@app.post("/api/v1/wallets/{WALLET_UUID}/operation",response_model=WalletOperation)
async def operate_wallet(WALLET_UUID: str, operation: WalletOperation):
    try:
        uuid = UUID_Type(WALLET_UUID)
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный UUID")
    try:
       result = await database.operation(UUID=uuid, operation_type=operation.operation_type, amount=operation.amount)

    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    except InsufficientFundsError:
        raise HTTPException(status_code=400, detail="Недостаточно средств")
    except Exception:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
    return WalletOperation(operation_type=result[0], amount=result[1])


@app.get("/api/v1/wallets/{WALLET_UUID}",response_model = WalletResponse)
async def get_wallet(WALLET_UUID: str):
    try:
        uuid = UUID_Type(WALLET_UUID)
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный UUID")
    try:
        balance = await database.get_wallet_balance(UUID=uuid)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return WalletResponse(uuid=uuid, balance=balance)
