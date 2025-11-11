# test_wallets.py
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4
from decimal import Decimal
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

client = TestClient(app)


def test_deposit_to_wallet():
    """Тест пополнения кошелька"""
    wallet_uuid = str(uuid4())
    response = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": "100.00"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == wallet_uuid
    assert Decimal(str(data["balance"])) == Decimal("100.00")


def test_withdraw_from_wallet():
    """Тест снятия средств с кошелька"""
    # Сначала пополним кошелек
    wallet_uuid = str(uuid4())
    client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": "200.00"}
    )

    # Теперь попробуем снять средства
    response = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": "50.00"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == wallet_uuid
    assert Decimal(str(data["balance"])) == Decimal("150.00")


def test_get_wallet_balance():
    """Тест получения баланса кошелька"""
    wallet_uuid = str(uuid4())
    # Сначала пополним кошелек
    client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": "300.00"}
    )

    # Получим баланс
    response = client.get(f"/api/v1/wallets/{wallet_uuid}")
    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == wallet_uuid
    assert Decimal(str(data["balance"])) == Decimal("300.00")


def test_invalid_uuid():
    """Тест с некорректным UUID"""
    response = client.post(
        "/api/v1/wallets/invalid-uuid/operation",
        json={"operation_type": "DEPOSIT", "amount": "100.00"}
    )
    assert response.status_code == 400


def test_insufficient_funds():
    """Тест попытки снятия средств больше, чем есть на балансе"""
    wallet_uuid = str(uuid4())
    # Попробуем снять средства с пустого кошелька
    response = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": "100.00"}
    )
    assert response.status_code == 400