# EV Charging Network Intelligence Platform

## Overview

This project is a smart city infrastructure platform designed to optimize a network of electric vehicle (EV) charging stations. It prevents grid overload, minimizes charging costs for consumers, and prioritizes the use of renewable energy by simulating real-time grid demand and calculating dynamic pricing. The entire system is built on a scalable, resilient microservices architecture orchestrated by Kubernetes.

## Architecture

The platform is composed of several independent microservices that communicate via REST APIs:

* **Station Service**: The system of record for all charging station data. It provides a full CRUD API for managing stations and is the only service that communicates directly with the database.
* **Demand Prediction Service**: Simulates real-time grid demand. This version uses the time of day to model peak and off-peak hours, providing a dynamic demand score.
* **Dynamic Pricing Service**: The system's brain. It consumes data from the Demand Service and uses it in a formula to calculate real-time, dynamic charging prices.
* **Frontend Dashboard**: A user-facing dashboard built with Next.js and TypeScript. It provides a real-time, interactive view of the station network and current grid pricing information.
* **PostgreSQL Database**: The persistent data store for all station-related information, running as a separate containerized service.

## Technology Stack

* **Backend**: Python (FastAPI)
* **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
* **Database**: PostgreSQL
* **Containerization**: Docker
* **Orchestration**: Kubernetes
* **Local Development**: Docker Compose

## Getting Started (Local Development)

To run the entire application stack locally for development.

### Prerequisites

* Docker Desktop installed and running.

### Steps

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:thedhinakarr/ev-charging-network.git
    cd ev-charging-network
    ```

2.  **Run the application with Docker Compose:**
    ```bash
    docker-compose -f docker-compose.dev.yml up --build
    ```
    Wait for all services to start.

3.  **Seed the database:**
    In a new terminal, run the seeder script to populate the database with sample stations.
    ```bash
    docker-compose -f docker-compose.dev.yml exec station-service python seed.py
    ```

4.  **Access the application:**
    Open your browser and navigate to **`http://localhost:3000`**.

## Kubernetes Deployment (Local)

To deploy the application to a local Kubernetes cluster (e.g., Docker Desktop).

### Prerequisites

* Docker Desktop installed with Kubernetes enabled.
* `kubectl` command-line tool configured to point to `docker-desktop`.
* A Docker Hub account (and you must be logged in via `docker login`).

### Steps

1.  **Build and Push Images:**
    Run the following commands to build and push the service images. Remember to update the image tags in the `k8s/*.yaml` files if you change them.
    ```bash
    # Example for one service
    docker build -t station-service ./services/station
    docker tag station-service dan210902/station-service:1.0.1
    docker push dan210902/station-service:1.0.1
    # (Repeat for all other services: demand, pricing, frontend)
    ```

2.  **Deploy to Kubernetes:**
    Apply all the Kubernetes manifest files.
    ```bash
    kubectl apply -f k8s/
    ```

3.  **Verify the Deployment:**
    Wait for all pods to be in the `Running` state.
    ```bash
    kubectl get pods -w
    ```

4.  **Seed the Database:**
    Get the name of a running `station-service` pod and run the seeder script.
    ```bash
    # Get pod name
    kubectl get pods
    # Run seeder (replace <pod-name>)
    kubectl exec <station-service-pod-name> -- python seed.py
    ```

5.  **Access the Application:**
    Open your browser and navigate to **`http://localhost:3000`**.

## Services

For more detailed information on each service, see their individual README files:
* [`services/frontend/README.md`](services/frontend/README.md)
* [`services/station/README.md`](services/station/README.md)
* [`services/demand/README.md`](services/demand/README.md)
* [`services/pricing/README.md`](services/pricing/README.md)