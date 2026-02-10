# 01_simple_reflex/Dockerfile

# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy the global requirements from the root context
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the shared logic and the specific agent code
COPY common/ ./common/
COPY 01_simple_reflex/ ./01_simple_reflex/

# Set the environment variable to ensure Python output isn't buffered
ENV PYTHONUNBUFFERED=1

# Run the agent
CMD ["python", "01_simple_reflex/agent.py"]