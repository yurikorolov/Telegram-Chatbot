# Use an official Python runtime as a parent image
FROM python:3.9

# Install system dependencies for ChromaDB
RUN apt-get update && apt-get install -y gcc python3-dev

# Now create user with host-mapped IDs
ARG USER_ID
ARG GROUP_ID
RUN addgroup --gid ${GROUP_ID} appuser && \
    adduser --disabled-password --gecos '' --uid ${USER_ID} --gid ${GROUP_ID} appuser

# Set the working directory in the container to /app
WORKDIR /app
# Create persistent storage directory and set permissions
RUN mkdir -p /app/persist && \
    chown appuser:appuser /app/persist

# Install hnswlib
RUN pip install hnswlib
    
COPY requirements.txt .
    
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y numpy \
    && pip install 'numpy<2.0.0'

# Copy files and transfer ownership
COPY ./main.py .
COPY ./memory.py .
COPY ./.env .
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Make port 80 available to the world outside this container
EXPOSE 80

# Start the application with the environment variable set
CMD ["python", "main.py"]
