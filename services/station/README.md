# Station Service

## Overview

The Station Service is the core data management component of the EV Charging Network Intelligence Platform. It acts as the single source of truth for all information related to physical charging stations. It is a stateless service that connects directly to the PostgreSQL database.

## Responsibilities

* Provides a full **CRUD (Create, Read, Update, Delete)** REST API for managing charging station records.
* Handles all direct database interactions using the SQLAlchemy ORM for safety and reliability.
* Serves station data to the frontend dashboard and any other services that may need it.

## API Endpoints

The service exposes the following RESTful endpoints:

| Method | Path                  | Description                        |
| :----- | :-------------------- | :--------------------------------- |
| `POST` | `/stations`           | Creates a new charging station.    |
| `GET`  | `/stations`           | Retrieves a list of all stations.  |
| `GET`  | `/stations/{station_id}` | Retrieves a single station by ID.  |
| `PUT`  | `/stations/{station_id}` | Updates an existing station's data. |
| `DELETE`| `/stations/{station_id}` | Deletes a station by ID.           |

### Sample Request Body for `POST /stations`

```json
{
  "name": "Downtown Public Library Charger",
  "location": "789 Knowledge Blvd, Central City",
  "status": "available",
  "power_kw": 50.0
}
```

-----

**Running Locally**

To run this service independently for development or testing, follow these steps:

**1. Navigate to the Directory**

```bash
cd services/station
```

**2. Set Up Virtual Environment & Install Dependencies**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Set Environment Variables**

```bash
export POSTGRES_HOST=localhost
export POSTGRES_USER=admin
export POSTGRES_PASSWORD=password123
export POSTGRES_DB=evcharging
```

**4. Run the Service**

```bash
uvicorn src.main:app --reload
```

The service will be available at `http://localhost:8000`.