
# Demand Prediction Service

## Overview

The Demand Prediction Service is a component of the EV Charging Network Intelligence Platform responsible for simulating real-time grid demand. It provides a simple REST API that returns a demand score, which other services can use to make intelligent decisions.

This implementation simulates demand based on the current time of day in Central Europe (CET), modeling morning/evening peak hours, daytime shoulder hours, and nighttime off-peak hours.

## Responsibilities

* To provide a dynamic, time-based demand score to any service that requests it.
* To encapsulate the logic for demand prediction, allowing it to be updated with a real machine-learning model in the future without affecting its consumers.

## API Endpoints

| Method | Path               | Description                                           |
| :----- | :----------------- | :---------------------------------------------------- |
| `GET`  | `/predict/demand`  | Returns the current simulated demand score and level. |

### Sample Response Body

```json
{
  "demand_score": 0.9,
  "demand_description": "Peak",
  "current_hour_cet": 18
}
````

## Running Locally

To run this service independently for development or testing:

1.  **Navigate to the Directory**

    ```bash
    cd services/demand
2.  **Set Up Virtual Environment & Install Dependencies**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Run the Service**

    ```bash
    uvicorn src.main:app --reload --port 8001
    ```

    The service will be available at `http://localhost:8001`.

<!-- end list -->
