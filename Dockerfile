# The builder image, used to build the virtual environment
FROM python:3.12-bookworm AS builder

# Install Poetry
RUN pip install --no-cache-dir poetry==1.8.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Dummy file to satisfy Poetry if README.md is required
RUN touch README.md

# Install Python dependencies
RUN poetry --version && poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to run the application
FROM python:3.12-slim-bookworm AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Copy the virtual environment from the builder stage
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy application code
COPY scraper ./scraper

# Set the entrypoint
ENTRYPOINT ["python", "-m", "scraper.main"]
