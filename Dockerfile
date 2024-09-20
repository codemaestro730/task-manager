# Use an official Python image (glibc based)
FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends gcc libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.8.3
RUN pip install "poetry==$POETRY_VERSION"
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Copy the project files
COPY pyproject.toml poetry.lock* /app/

# Install project dependencies
RUN poetry install --no-dev --no-root

COPY . /app/

# Command to run the application
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]