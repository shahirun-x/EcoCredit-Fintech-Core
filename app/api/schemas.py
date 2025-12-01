from pydantic import BaseModel, Field
from typing import Optional

# 1. Input Schema: What the Frontend sends us
class TransactionRequest(BaseModel):
    description: str = Field(..., example="UBER *TRIP 8412")
    amount: float = Field(..., gt=0, example=14.20)
    currency: str = Field("USD", max_length=3, example="USD")

# 2. Output Schema: What we send back
class CarbonReport(BaseModel):
    category: str
    reasoning: str
    carbon_kg: float
    # We add a "Green Score" (0-10) just for the UI
    green_score: float