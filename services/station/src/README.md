
# Code Documentation: `station-service/src/main.py`

This document provides a detailed explanation of the source code for the Station Service.

## 1. Imports and Setup

```python
import os
import time
from contextlib import asynccontextmanager
# ... other imports
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import sessionmaker, Session, declarative_base
````

The script begins by importing all necessary libraries.

  * **FastAPI & Pydantic**: For building the web server and for data validation.
  * **SQLAlchemy**: The Object-Relational Mapper (ORM) used to interact with the PostgreSQL database in a safe and Pythonic way.
  * **Standard Libraries**: `os` for reading environment variables, `time` for handling delays, etc.

## 2\. Database Configuration

```python
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password123")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres-service")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "evcharging")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

This section sets up the database connection.

  * It reads each part of the connection string from **environment variables**, providing sensible defaults. This makes the service configurable and portable between different environments (like Docker Compose and Kubernetes).
  * It assembles the final `DATABASE_URL`.
  * It creates a SQLAlchemy `engine` to manage connections and a `SessionLocal` factory to create database sessions for each request.

## 3\. ORM Model and Pydantic Schemas

### `Station` (SQLAlchemy Model)

```python
class Station(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True, index=True)
    # ... other columns
```

This class defines the structure of the `stations` table in the database. SQLAlchemy uses this model to map Python objects to database rows.

### `Station...Schema` (Pydantic Models)

```python
class StationCreateSchema(BaseModel):
    # ... fields
class StationResponseSchema(BaseModel):
    # ... fields
    class Config:
        from_attributes = True
```

These classes define the data shapes for our API.

  * `StationCreateSchema` and `StationUpdateSchema` validate incoming data from `POST` and `PUT` requests.
  * `StationResponseSchema` defines the structure of data sent back to the client. The `Config.from_attributes = True` setting is crucial; it allows Pydantic to automatically create these schemas from the SQLAlchemy `Station` model objects.

## 4\. Lifespan Manager

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ... retry logic ...
    try:
        Base.metadata.create_all(bind=engine)
    # ...
    yield
    # ...
```

The `lifespan` function is a modern FastAPI feature that runs code on application startup and shutdown.

  * **Startup Logic**: On startup, it enters a **resilient retry loop**. It attempts to connect to the database and create the `stations` table if it doesn't exist. If the connection fails (e.g., because the database container is still initializing), it waits 5 seconds and tries again, up to 5 times. This makes the service robust in a distributed environment.
  * **Shutdown Logic**: Code after the `yield` statement would run when the application shuts down.

## 5\. API Endpoints

```python
@app.get("/stations", response_model=List[StationResponseSchema])
def get_all_stations(db: Session = Depends(get_db)):
    return db.query(Station).all()
```

Each function defines a REST API endpoint.

  * The `@app.get`, `@app.post`, etc., decorators from FastAPI define the path and HTTP method.
  * `response_model` tells FastAPI to validate the outgoing data against our Pydantic schema.
  * `db: Session = Depends(get_db)` is the **Dependency Injection** system. It provides a clean, managed database session to the function and guarantees that the session is closed after the request is complete, preventing resource leaks.
  * The function body contains the business logic, using the SQLAlchemy session (`db`) to query or modify data.

