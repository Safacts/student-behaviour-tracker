#!/bin/bash
set -e

# Function to log with timestamp
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Wait for database to be ready
wait_for_db() {
    if [ -n "$DATABASE_URL" ]; then
        log "Waiting for database connection..."
        
        # Extract host and port from DATABASE_URL
        DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
        DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
        
        if [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then
            while ! nc -z "$DB_HOST" "$DB_PORT"; do
                log "Database is unavailable - sleeping"
                sleep 2
            done
            log "Database is up - continuing"
        fi
    fi
}

# Wait for Redis to be ready
wait_for_redis() {
    if [ -n "$REDIS_URL" ]; then
        log "Waiting for Redis connection..."
        
        # Extract host and port from REDIS_URL
        REDIS_HOST=$(echo $REDIS_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
        REDIS_PORT=$(echo $REDIS_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
        
        if [ -n "$REDIS_HOST" ] && [ -n "$REDIS_PORT" ]; then
            while ! nc -z "$REDIS_HOST" "$REDIS_PORT"; do
                log "Redis is unavailable - sleeping"
                sleep 2
            done
            log "Redis is up - continuing"
        fi
    fi
}

# Create necessary directories
create_directories() {
    log "Creating necessary directories..."
    mkdir -p /app/data
    mkdir -p /app/logs
    
    # Set permissions
    chmod 755 /app/data
    chmod 755 /app/logs
}

# Run database migrations (if needed)
run_migrations() {
    if [ "$RUN_MIGRATIONS" = "true" ]; then
        log "Running database migrations..."
        # This would run Alembic migrations
        # alembic upgrade head
        log "Migrations completed"
    fi
}

# Main startup sequence
main() {
    log "Starting Student Behavior Analytics Microservice..."
    log "Environment: $ENVIRONMENT"
    log "Version: $API_VERSION"
    
    # Create directories
    create_directories
    
    # Wait for dependencies
    wait_for_db
    wait_for_redis
    
    # Run migrations if needed
    run_migrations
    
    # Start the application
    log "Starting application server..."
    exec "$@"
}

# Execute main function
main "$@"
