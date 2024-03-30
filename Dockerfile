# Use the official Python image as the base image
FROM python:3.9-slim

# Install nmap package
RUN apt-get update && apt-get install -y nmap

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the Flask port
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
