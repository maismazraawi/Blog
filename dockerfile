# Use an official Python base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy only the pyproject.toml and poetry.lock to leverage caching
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the rest of the application files
COPY . /app

# Expose the port your app runs on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "blog.main:app", "--host", "0.0.0.0", "--port", "8000"]