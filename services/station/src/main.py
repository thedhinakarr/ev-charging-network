# services/station/src/main.py
import os
import time
from contextlib import asynccontextmanager
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# --- Corrected Database Configuration ---
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password123")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres-service")
DB_PORT = os.getenv("POSTGRES_PORT", "5432") # <-- THIS LINE IS THE FIX
DB_NAME = os.getenv("POSTGRES_DB", "evcharging")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- The rest of the file is correct and unchanged ---
class Station(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    status = Column(String, default="available")
    power_kw = Column(Float, default=50.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class StationCreateSchema(BaseModel): name: str; location: str; status: str = "available"; power_kw: float = 50.0
class StationUpdateSchema(BaseModel): name: Optional[str] = None; location: Optional[str] = None; status: Optional[str] = None; power_kw: Optional[float] = None
class StationResponseSchema(BaseModel):
    id: int; name: str; location: str; status: str; power_kw: float; created_at: datetime
    class Config: from_attributes = True

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    db_connected = False; retries = 5
    while not db_connected and retries > 0:
        try:
            Base.metadata.create_all(bind=engine)
            print("Database connection successful. Tables created.")
            db_connected = True
        except Exception as e:
            print(f"Database connection failed: {e}"); retries -= 1
            print(f"Retrying connection... {retries} attempts left."); time.sleep(5)
    yield
    print("Application shutdown.")

app = FastAPI(title="Station Service", description="Manages EV charging station data.", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/")
def read_root(): return {"status": "ok", "service": "Station Service"}
@app.post("/stations", response_model=StationResponseSchema, status_code=status.HTTP_201_CREATED)
def create_station(station: StationCreateSchema, db: Session = Depends(get_db)):
    new_station = Station(**station.model_dump()); db.add(new_station); db.commit(); db.refresh(new_station); return new_station
@app.get("/stations", response_model=List[StationResponseSchema])
def get_all_stations(db: Session = Depends(get_db)): return db.query(Station).all()
@app.get("/stations/{station_id}", response_model=StationResponseSchema)
def get_station_by_id(station_id: int, db: Session = Depends(get_db)):
    station = db.query(Station).filter(Station.id == station_id).first()
    if not station: raise HTTPException(status_code=404, detail="Station not found")
    return station
@app.put("/stations/{station_id}", response_model=StationResponseSchema)
def update_station(station_id: int, station_update: StationUpdateSchema, db: Session = Depends(get_db)):
    station_to_update = db.query(Station).filter(Station.id == station_id).first()
    if not station_to_update: raise HTTPException(status_code=404, detail="Station not found")
    update_data = station_update.model_dump(exclude_unset=True)
    for key, value in update_data.items(): setattr(station_to_update, key, value)
    db.commit(); db.refresh(station_to_update); return station_to_update
@app.delete("/stations/{station_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_station(station_id: int, db: Session = Depends(get_db)):
    station_to_delete = db.query(Station).filter(Station.id == station_id).first()
    if not station_to_delete: raise HTTPException(status_code=404, detail="Station not found")
    db.delete(station_to_delete); db.commit(); return Response(status_code=status.HTTP_204_NO_CONTENT)