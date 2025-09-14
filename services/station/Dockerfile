# services/station/Dockerfile

FROM python:3.11-slim
WORKDIR /app

# Copy requirements first for better caching
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- ADD THIS LINE ---
# Copy the seed script into the container's working directory (/app)
COPY ./seed.py .

# Copy the rest of the application's code
COPY ./src ./src

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]