# Use the Python 3.12 slim base image
FROM python:3.12-slim

# Set environment variables to prevent prompts during installation
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Create app directory and copy project files
WORKDIR /app
COPY . .

# Install project dependencies using Poetry
RUN poetry install --no-root

# Expose the FastAPI port (default is 8000)
EXPOSE 8000

# Start FastAPI server
CMD ["poetry", "run", "uvicorn", "blog.main:app", "--host", "0.0.0.0", "--port", "8000"]
