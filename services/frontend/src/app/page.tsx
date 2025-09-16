'use client';

import { useEffect, useState, useCallback } from 'react';

// Define types for our data
type Station = {
  id: number;
  name: string;
  location: string;
  status: string;
  power_kw: number;
};

type Pricing = {
  price_per_kwh: number;
  based_on_demand: {
    demand_description: string;
  };
};

export default function HomePage() {
  const [stations, setStations] = useState<Station[]>([]);
  const [pricing, setPricing] = useState<Pricing | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // --- THIS IS THE CHANGE ---
  // The URLs now point to the NodePort addresses that will be exposed on localhost.
  // These are provided by the environment variables in the frontend-deployment.yaml.
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const pricingApiUrl = process.env.NEXT_PUBLIC_PRICING_API_URL || 'http://localhost:8002';

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [stationRes, pricingRes] = await Promise.all([
        fetch(`${apiUrl}/stations`),
        fetch(`${pricingApiUrl}/pricing/current`)
      ]);
      if (!stationRes.ok || !pricingRes.ok) {
        throw new Error('Failed to fetch data from the APIs.');
      }
      const stationData: Station[] = await stationRes.json();
      const pricingData: Pricing = await pricingRes.json();
      setStations(stationData);
      setPricing(pricingData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred.');
    } finally {
      setIsLoading(false);
    }
  }, [apiUrl, pricingApiUrl]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleDelete = async (stationId: number) => {
    setStations(stations.filter(station => station.id !== stationId));
    try {
      const response = await fetch(`${apiUrl}/stations/${stationId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Failed to delete station. Please refresh.');
      }
    } catch (err) {
       setError(err instanceof Error ? err.message : 'An unknown error occurred.');
    }
  };

  return (
    <main className="container mx-auto p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800">EV Charging Network Dashboard</h1>
        <button
          onClick={fetchData}
          disabled={isLoading}
          className="px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 disabled:bg-indigo-300 transition-colors"
        >
          {isLoading ? 'Refreshing...' : 'Refresh Data'}
        </button>
      </div>
      
      <div className="grid md:grid-cols-3 gap-8">
        <div className="md:col-span-2 bg-white shadow-md rounded-lg p-6">
          <h2 className="text-2xl font-semibold mb-4 text-gray-700">Live Station Status</h2>
          {error && <p className="text-red-500 font-bold mb-4">Error: {error}</p>}
          <ul className="space-y-4">
            {stations.map((station) => (
              <li key={station.id} className="p-4 border rounded-md flex justify-between items-center group">
                <div>
                  <p className="font-semibold text-lg">{station.name}</p>
                  <p className="text-sm text-gray-600">{station.location}</p>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <span className={`px-3 py-1 text-sm font-medium rounded-full ${ station.status === 'available' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800' }`}>
                      {station.status}
                    </span>
                    <p className="text-xs text-gray-500 mt-1">{station.power_kw} kW</p>
                  </div>
                  <button
                    onClick={() => handleDelete(station.id)}
                    className="px-3 py-1 bg-red-100 text-red-700 text-xs font-bold rounded-full opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-200"
                  >
                    DELETE
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </div>
        <div className="bg-gray-50 shadow-md rounded-lg p-6">
          <h2 className="text-2xl font-semibold mb-4 text-gray-700">Grid Info</h2>
          {pricing && (
            <div className="text-center">
              <p className="text-gray-600 text-lg">Current Price</p>
              <p className="text-5xl font-bold text-indigo-600 my-2">${pricing.price_per_kwh.toFixed(2)}</p>
              <p className="text-gray-600 text-lg">per kWh</p>
              <div className="mt-6">
                <p className="text-sm text-gray-500">Based on Demand:</p>
                <p className="font-semibold text-xl text-gray-800 capitalize">{pricing.based_on_demand.demand_description}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}