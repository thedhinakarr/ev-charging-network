
# Dynamic Pricing Service

## Overview

The Dynamic Pricing Service is the calculation engine for the EV Charging Network Intelligence Platform. It is responsible for determining the real-time cost of charging based on current grid conditions.

This service demonstrates a key microservice pattern: **inter-service communication**. It programmatically calls the `demand-service`'s API to fetch the current demand score. It then uses this score in a pricing formula to calculate the final price per kWh.

## Responsibilities

* To provide a REST API endpoint for fetching the current, dynamically calculated charging price.
* To consume data from the `demand-service` to inform its pricing logic.
* To encapsulate all pricing-related business logic, allowing the formula to be changed in the future without impacting any other service.

## API Endpoints

| Method | Path                | Description                                                |
| :----- | :------------------ | :--------------------------------------------------------- |
| `GET`  | `/pricing/current`  | Returns the current calculated price based on grid demand. |

### Sample Response Body

The response includes the final price and, for transparency, the demand data that was used in the calculation.

```json
{
  "price_per_kwh": 0.65,
  "based_on_demand": {
    "demand_score": 0.9,
    "demand_description": "Peak",
    "current_hour_cet": 17
  }
}
````

## Running Locally

To run this service independently for development or testing:

1.  **Navigate to the Directory**

    ```bash
    cd services/pricing

2.  **Set Up Virtual Environment & Install Dependencies**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

3.  **Run the Service**
    *Note: This service requires the `demand-service` to be running and accessible at `http://localhost:8001` for it to function correctly.*

    ```bash
    uvicorn src.main:app --reload --port 8002

    The service will be available at `http://localhost:8002`.

<!-- end list -->
