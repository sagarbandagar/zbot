# Use Python 3.11 as base image (like installing Python on a fresh computer)
FROM python:3.11-slim

# Set working directory inside container (like creating a folder to work in)
WORKDIR /app

# Copy requirements first (this helps Docker cache better - saves time on rebuilds)
COPY requirement.txt .

# Install Python packages (like pip install on your computer)
RUN pip install --no-cache-dir -r requirement.txt

# Copy all your app code to the container
COPY . .

# Tell Docker which port your app uses (FastAPI usually runs on 8000)
EXPOSE 8000

# Command to run when container starts (like running python main.py)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
