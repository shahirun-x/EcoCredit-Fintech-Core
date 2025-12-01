from fastapi import APIRouter, HTTPException
from app.api.schemas import TransactionRequest, CarbonReport
from app.agents.transaction_agent import TransactionAgent
from app.services.climatiq_client import ClimatiqClient

router = APIRouter()

# Initialize our tools once (Singleton pattern)
agent = TransactionAgent()
carbon_engine = ClimatiqClient()

@router.post("/analyze", response_model=CarbonReport)
async def analyze_transaction(request: TransactionRequest):
    """
    Industrial Workflow:
    1. Agent classifies the transaction (Ambiguity Resolution)
    2. Engine calculates the exact Carbon Footprint (Scientific Data)
    """
    
    # Step 1: AI Classification
    print(f"🧠 Analyzing: {request.description}...")
    ai_result = agent.categorize(request.description, request.amount, request.currency)
    
    category = ai_result.get("category", "Unknown")
    reasoning = ai_result.get("reasoning", "Analysis failed")
    
    # Step 2: Carbon Calculation
    print(f"🌍 Calculating Carbon for: {category}...")
    carbon_result = carbon_engine.get_carbon_estimate(category, request.amount, request.currency)
    
    co2 = carbon_result.get("co2_kg", 0)
    
    # Simple algorithm for "Green Score" (Lower CO2 = Higher Score)
    # In a real bank, this would be a complex risk model
    green_score = max(0, 10 - (co2 / 5)) # Simple formula: 10 minus (CO2/5)

    return CarbonReport(
        category=category,
        reasoning=reasoning,
        carbon_kg=round(co2, 2),
        green_score=round(green_score, 1)
    )