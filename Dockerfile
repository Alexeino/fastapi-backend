# Stage 1: Build the application
FROM python:3.10-alpine as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies
RUN apk add --update --virtual .build-deps \
    build-base \
    postgresql-dev \
    python3-dev \
    libpq

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./ 

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile --system

# Stage 2: Create the final image
FROM python:3.10-alpine

# Install runtime dependencies
RUN apk add --no-cache libpq

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY . /app
WORKDIR /app

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Make the script executable
RUN chmod +x /app/entrypoint.sh

EXPOSE 10000

# Use entrypoint.sh for migrations and starting the server
ENTRYPOINT ["/app/entrypoint.sh"]
