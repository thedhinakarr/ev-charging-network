# Station Service

Manages charging station data and real-time availability.

## Responsibilities
- Track charging station locations and capacity
- Monitor real-time availability
- Provide station search and filtering
- Integration with external charging networks

## API Endpoints
- GET /api/stations - List all stations
- GET /api/stations/{id} - Get station details
- GET /api/stations/nearby - Find nearby stations

## Development
```bash
cd services/station
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

