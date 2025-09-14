# services/station/src/main.py
import os
from contextlib import asynccontextmanager
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# --- Database Setup (SQLAlchemy ORM) ---

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password123@postgres:5432/evcharging")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- ORM Model (Database Table Representation) ---

class Station(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    status = Column(String, default="available")
    power_kw = Column(Float, default=50.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# --- Pydantic Schemas (API Data Shapes) ---

# Schema for creating a station (input)
class StationCreateSchema(BaseModel):
    name: str
    location: str
    status: str = "available"
    power_kw: float = 50.0

# Schema for updating a station (input, all fields are optional)
class StationUpdateSchema(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    power_kw: Optional[float] = None

# Schema for API responses (output)
class StationResponseSchema(BaseModel):
    id: int
    name: str
    location: str
    status: str
    power_kw: float
    created_at: datetime

    class Config:
        from_attributes = True

# --- Lifespan Manager (Startup/Shutdown Logic) ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup: Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    if db.query(Station).count() == 0:
        print("Seeding database with initial stations...")
        seed_stations = [
            Station(name="City Hall Charger 1", location="123 Main St", status="available", power_kw=50),
            Station(name="Library Charger A", location="456 Oak Ave", status="charging", power_kw=150)
        ]
        db.add_all(seed_stations)
        db.commit()
    db.close()
    
    yield
    print("Application shutdown.")

# --- FastAPI Application ---

app = FastAPI(
    title="Station Service",
    description="Manages EV charging station data.",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Dependency ---

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints (Full CRUD) ---

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Station Service"}

# CREATE a new station
@app.post("/stations", response_model=StationResponseSchema, status_code=status.HTTP_201_CREATED)
def create_station(station: StationCreateSchema, db: Session = Depends(get_db)):
    new_station = Station(**station.model_dump())
    db.add(new_station)
    db.commit()
    db.refresh(new_station)
    return new_station

# READ all stations
@app.get("/stations", response_model=List[StationResponseSchema])
def get_all_stations(db: Session = Depends(get_db)):
    stations = db.query(Station).all()
    return stations

# READ a single station by its ID
@app.get("/stations/{station_id}", response_model=StationResponseSchema)
def get_station_by_id(station_id: int, db: Session = Depends(get_db)):
    station = db.query(Station).filter(Station.id == station_id).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return station

# UPDATE a station by its ID
@app.put("/stations/{station_id}", response_model=StationResponseSchema)
def update_station(station_id: int, station_update: StationUpdateSchema, db: Session = Depends(get_db)):
    station_to_update = db.query(Station).filter(Station.id == station_id).first()
    if not station_to_update:
        raise HTTPException(status_code=404, detail="Station not found")
    
    update_data = station_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(station_to_update, key, value)
        
    db.commit()
    db.refresh(station_to_update)
    return station_to_update

# DELETE a station by its ID
@app.delete("/stations/{station_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_station(station_id: int, db: Session = Depends(get_db)):
    station_to_delete = db.query(Station).filter(Station.id == station_id).first()
    if not station_to_delete:
        raise HTTPException(status_code=404, detail="Station not found")
        
    db.delete(station_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)