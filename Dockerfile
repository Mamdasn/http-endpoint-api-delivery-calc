# syntax=docker/dockerfile:1

FROM python:3.11-alpine

# Create a home directory for the new user called appuser
RUN adduser -D appuser

# Set the user to appuser
USER appuser

# Add ~/.local/bin to the PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Set the working directory inside the container
WORKDIR /home/appuser

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install any dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose port 5000 of the container
EXPOSE 5000

# Specify the command to run on container start
CMD ["sh", "-c", "uvicorn --workers 1 --host 0.0.0.0 --port 5000 api_app:app"]
