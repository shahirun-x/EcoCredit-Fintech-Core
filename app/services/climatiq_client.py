import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ClimatiqClient:
    def __init__(self):
        self.api_key = os.getenv("CLIMATIQ_API_KEY")
        self.base_url = "https://api.climatiq.io/data/v1"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        # In a real app, we would cache these IDs in Redis to save API calls
        self.id_cache = {} 

    def _find_activity_id(self, query: str):
        """
        Dynamically searches for a valid Spend-based Activity ID.
        This prevents 'ID Not Found' errors by asking the API what exists.
        """
        if query in self.id_cache:
            return self.id_cache[query]

        url = f"{self.base_url}/search"
        params = {
            "query": query,
            "unit_type": "Money", # CRITICAL: Only get IDs that accept $$$
            "data_version": "^5",  # Use dynamic versioning
            "results_per_page": 1
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            results = response.json().get("results", [])
            
            if not results:
                return None
            
            # Grab the first valid ID
            activity_id = results[0]["activity_id"]
            self.id_cache[query] = activity_id # Cache it
            print(f"✅ Found ID for '{query}': {activity_id}")
            return activity_id
            
        except Exception as e:
            print(f"⚠️ Search failed for '{query}': {e}")
            return None

    def get_carbon_estimate(self, category: str, amount: float, currency: str = "USD"):
        # Map simple categories to Search Queries
        search_terms = {
            "Fuel": "petrol",
            "Groceries": "food products",
            "Dining": "restaurants",
            "Travel": "taxi",
            "Clothing": "textiles",
            "Electronics": "computer equipment",
            "Unknown": "consumer goods"
        }

        search_query = search_terms.get(category, "consumer goods")
        
        # 1. Dynamically find the ID
        activity_id = self._find_activity_id(search_query)
        
        if not activity_id:
            # Fallback if search fails completely
            return {"co2_kg": 0, "error": "Could not find valid Activity ID"}

        # 2. Calculate Carbon
        payload = {
            "emission_factor": {
                "activity_id": activity_id,
                "data_version": "^5" # Must match the search version
            },
            "parameters": {
                "money": amount,
                "money_unit": currency.lower()
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/estimate",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "co2_kg": data.get("co2e", 0),
                "category": category,
                "activity_id": activity_id
            }
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ Estimate Error: {response.text}") 
            return {"co2_kg": 0, "error": response.text}

if __name__ == "__main__":
    client = ClimatiqClient()
    print("Testing Dynamic Engine...")
    
    # Test 1: Dining
    print(client.get_carbon_estimate("Dining", 25))
    
    # Test 2: Fuel
    print(client.get_carbon_estimate("Fuel", 50))