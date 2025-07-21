# Use a base Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for Selenium and Firefox
RUN apt-get update && apt-get install -y \
    wget \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Install Python libraries
RUN pip install selenium

# Copy the Python script into the container
COPY main.py .

# Command to run the script
CMD ["python", "main.py"]