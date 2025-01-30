# Use an official Python runtime as a parent image
FROM python:3.9

# Set build arguments for user/group IDs
ARG USER_ID
ARG GROUP_ID

# Install system dependencies for ChromaDB
RUN apt-get update && apt-get install -y gcc python3-dev

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY ./main.py .
COPY ./memory.py .
COPY requirements.txt .

# Create persistent storage directory
RUN mkdir -p /app/persist

# Install hnswlib
RUN pip install hnswlib

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y numpy \
    && pip install 'numpy<2.0.0'

# Make port 80 available to the world outside this container
EXPOSE 80

# Start the application with the environment variable set
CMD ["python", "main.py"]
