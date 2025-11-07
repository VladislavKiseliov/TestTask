from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal

class WalletOperation(BaseModel):
    operation_type: str = Field(pattern="^(DEPOSIT|WITHDRAW)$")
    amount: Decimal = Field(gt=0, max_digits=18, decimal_places=2)

class WalletResponse(BaseModel):
    uuid: UUID
    balance: Decimal






