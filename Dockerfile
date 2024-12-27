# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code
COPY . .

# Make wait script executable
RUN chmod +x wait-for-db.sh

# Expose the port the app runs on
EXPOSE 5555

# Command to run the application
CMD ["./wait-for-db.sh"]
