# services/pricing/src/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI(title="Pricing Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

DEMAND_SERVICE_URL = "http://demand-service:8001/predict/demand"

# Define base price and a surcharge for peak demand
BASE_PRICE_PER_KWH = 0.20
PEAK_SURCHARGE_MULTIPLIER = 0.50

@app.get("/pricing/current")
def get_current_pricing():
    """
    Calculates dynamic pricing based on a formula using the demand score.
    """
    try:
        response = requests.get(DEMAND_SERVICE_URL)
        response.raise_for_status()
        demand_data = response.json()
        demand_score = demand_data.get("demand_score", 0.5)

        # Formula: price = base_price + (demand_score * surcharge)
        calculated_price = BASE_PRICE_PER_KWH + (demand_score * PEAK_SURCHARGE_MULTIPLIER)

        return {
            "price_per_kwh": round(calculated_price, 4),
            "based_on_demand": demand_data
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Demand service unavailable: {e}")