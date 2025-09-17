# Frontend Dashboard

## Overview

The Frontend Dashboard is the user interface for the EV Charging Network Intelligence Platform. It provides a real-time, interactive, single-page application for operators to monitor the network's status and grid information.

The dashboard is built with Next.js, React, and TypeScript, and styled with Tailwind CSS for a modern and responsive design.

## Features

* **Live Station Monitoring**: Displays a real-time list of all charging stations, including their name, location, operational status, and power rating.
* **Dynamic Grid Information**: Shows a dynamically updated charging price and the current grid demand level (e.g., "Peak", "Off-Peak") used to calculate the price.
* **Interactive Controls**: Features a "Refresh Data" button to fetch the latest information on demand and a "Delete" button for each station to demonstrate live interaction with the backend API.

## Technology Stack

* **Framework**: Next.js 14
* **Language**: TypeScript
* **UI Library**: React
* **Styling**: Tailwind CSS

## API Consumption

The frontend is a pure client of the backend microservices. It consumes data from two primary REST APIs:
* **Station Service**: To fetch and manage the list of charging stations.
* **Pricing Service**: To fetch the real-time, dynamic charging price and demand level.

## Running Locally

To run this service independently for development:

1.  **Navigate to the Directory**
    ```bash
    cd services/frontend
    ```

2.  **Install Dependencies**
    This project uses `pnpm` for package management.
    ```bash
    npm install -g pnpm
    pnpm install
    ```

3.  **Run the Development Server**
    *Note: For the application to be fully functional, the `station-service` and `pricing-service` must be running and accessible on their respective ports.*
    ```bash
    pnpm run dev
    ```
    The application will be available at `http://localhost:3000`.