# ev-charging-network
Smart EV charging optimization system with microservices and Kubernetes
# EV Charging Network Intelligence Platform

## Overview
Smart city infrastructure platform that optimizes electric vehicle charging to prevent grid overload while minimizing costs and maximizing renewable energy usage.

## Architecture
- **Station Service**: Manages charging station data and availability
- **Demand Prediction Service**: Forecasts charging demand using ML algorithms  
- **Dynamic Pricing Service**: Calculates real-time pricing based on demand and grid conditions
- **Frontend Dashboard**: Real-time visualization with Next.js and TypeScript
- **PostgreSQL Database**: Persistent data storage

## Technology Stack
- **Backend**: Python (FastAPI/Flask)
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Database**: PostgreSQL
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Deployment**: Local Kubernetes (Docker Desktop)

## Project Status
**In Development** - Setting up foundation

## Getting Started
*Coming soon...*

## Documentation
- [Architecture Overview](docs/architecture/README.md)
- [API Documentation](docs/api/README.md)
- [Deployment Guide](docs/deployment.md)

## Services
- [Station Service](services/station/README.md)
- [Demand Prediction Service](services/demand/README.md)
- [Pricing Service](services/pricing/README.md)
- [Frontend Dashboard](services/frontend/README.md)