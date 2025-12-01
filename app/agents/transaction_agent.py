import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate # <--- UPDATED IMPORT
from dotenv import load_dotenv

load_dotenv()

class TransactionAgent:
    def __init__(self):
        # We use a lower temperature (0) for deterministic, factual outputs
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
        
        # This prompt forces the LLM to act as a Bank Analyst
        self.template = """
        You are a Senior Data Analyst at a Fintech Bank.
        Your job is to categorize raw transaction strings into Carbon Categories.
        
        VALID CATEGORIES:
        - Fuel (Gas stations, EV charging)
        - Groceries (Supermarkets, convenience stores)
        - Dining (Restaurants, fast food, cafes)
        - Travel (Uber, flights, trains, public transport)
        - Clothing (Apparel, fashion)
        - Electronics (Gadgets, software subscriptions)
        - Unknown (If you are less than 80% sure)

        RULES:
        1. Analyze the 'description' and 'amount' to guess the context.
        2. Example: "Shell" with $5.00 is likely 'Groceries' (snack), but "Shell" with $40.00 is 'Fuel'.
        3. Return ONLY a valid JSON object with keys: "category" and "reasoning".
        4. Do not output markdown ticks (```json). Just the raw JSON string.

        Transaction Description: {description}
        Amount: {amount}
        Currency: {currency}

        JSON Output:
        """
        
        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=["description", "amount", "currency"]
        )

    def categorize(self, description: str, amount: float, currency: str = "USD"):
        # Create the chain
        chain = self.prompt | self.llm
        
        try:
            # Run the agent
            response = chain.invoke({
                "description": description, 
                "amount": amount, 
                "currency": currency
            })
            
            # Clean the output (sometimes LLMs add ```json ... ```)
            clean_json = response.content.replace("```json", "").replace("```", "").strip()
            
            # Parse into a real Python dictionary
            return json.loads(clean_json)
            
        except Exception as e:
            print(f"❌ Agent Error: {e}")
            return {"category": "Unknown", "reasoning": "Agent failed to parse"}

if __name__ == "__main__":
    agent = TransactionAgent()
    print("Testing AI Analyst...")
    
    # Test 1: The Ambiguous "Shell" Case (Snack)
    print("\nTest 1 (Snack at Gas Station):")
    print(agent.categorize("SHELL STATION 402", 5.50))
    
    # Test 2: The Ambiguous "Shell" Case (Fuel)
    print("\nTest 2 (Actual Gas):")
    print(agent.categorize("SHELL STATION 402", 45.00))
    
    # Test 3: Messy Data
    print("\nTest 3 (Messy Uber):")
    print(agent.categorize("UBER *TRIP 8412 HELP.UBER", 14.20))