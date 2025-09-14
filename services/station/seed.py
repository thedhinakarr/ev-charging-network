import os
import psycopg2
from faker import Faker
import random

# Initialize Faker for realistic data
fake = Faker()

# Database connection details from environment variables
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "evcharging")
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password123")

def seed_data():
    """Connects to the database and populates the stations table."""
    conn = None
    try:
        # Establish connection
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()

        # Clear existing data to prevent duplicates on re-runs
        cur.execute("TRUNCATE TABLE stations RESTART IDENTITY CASCADE;")
        print("Cleared existing station data.")

        # Generate and insert 20 sample stations
        stations_to_insert = []
        statuses = ["available", "charging", "offline"]
        power_ratings = [22, 50, 150, 350]

        for _ in range(20):
            name = f"{fake.street_name()} SuperCharger"
            location = fake.address().replace('\n', ', ')
            status = random.choice(statuses)
            power_kw = random.choice(power_ratings)
            stations_to_insert.append((name, location, status, power_kw))

        # Use execute_values for efficient bulk insert
        from psycopg2.extras import execute_values
        execute_values(
            cur,
            "INSERT INTO stations (name, location, status, power_kw) VALUES %s",
            stations_to_insert
        )
        
        conn.commit()
        print(f"Successfully inserted {len(stations_to_insert)} stations.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    seed_data()