# services/demand/src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random # Make sure random is imported

app = FastAPI(title="Demand Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Define our possible demand scenarios
DEMAND_SCENARIOS = [
    {"demand_score": 0.9, "demand_description": "Peak"},
    {"demand_score": 0.5, "demand_description": "Shoulder"},
    {"demand_score": 0.2, "demand_description": "Off-Peak"},
]

@app.get("/predict/demand")
def predict_demand():
    """
    Simulates demand by RANDOMLY choosing a scenario.
    """
    # Randomly choose one of the scenarios
    scenario = random.choice(DEMAND_SCENARIOS)

    return {
        "demand_score": scenario["demand_score"],
        "demand_description": scenario["demand_description"],
        "timestamp": datetime.now().isoformat()
    }