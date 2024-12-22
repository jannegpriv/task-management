# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install wget for downloading wait-for-it
RUN apt-get update && apt-get install -y wget

# Download wait-for-it script
RUN wget -O /wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /wait-for-it.sh

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code
COPY . .

# Expose the port the app runs on
EXPOSE 5555

# Command to run the application
CMD ["/bin/bash", "-c", "/wait-for-it.sh db:5432 -t 60 -- python main.py"]
