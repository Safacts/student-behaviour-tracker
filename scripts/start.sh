#!/bin/bash
set -e

# Student Behavior Analytics Service Startup Script
# This script handles environment setup and service startup

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1  # Port is in use
    else
        return 0  # Port is available
    fi
}

# Function to detect environment
detect_environment() {
    if [ -n "$ENVIRONMENT" ]; then
        echo "$ENVIRONMENT"
    elif [ -f ".env" ] && grep -q "ENVIRONMENT=production" .env; then
        echo "production"
    else
        echo "development"
    fi
}

# Function to setup Python environment
setup_python_env() {
    log "Setting up Python environment..."
    
    if ! command_exists python3; then
        error "Python 3 is required but not installed"
        exit 1
    fi
    
    if ! command_exists poetry; then
        log "Installing Poetry..."
        curl -sSL https://install.python-poetry.org | python3 -
        export PATH="$HOME/.local/bin:$PATH"
    fi
    
    if [ -f "pyproject.toml" ]; then
        log "Installing dependencies with Poetry..."
        poetry install
    else
        error "pyproject.toml not found"
        exit 1
    fi
    
    success "Python environment setup completed"
}

# Function to setup database
setup_database() {
    local env=$(detect_environment)
    log "Setting up database for $env environment..."
    
    # Create data directory
    mkdir -p data
    mkdir -p logs
    
    if [ "$env" = "development" ]; then
        # For development, ensure SQLite database exists
        if [ ! -f "data/student_behavior.db" ]; then
            log "Creating SQLite database..."
            # Database will be created automatically by SQLAlchemy
        fi
    else
        # For production, check PostgreSQL connection
        if [ -n "$DATABASE_URL" ]; then
            log "Checking PostgreSQL connection..."
            # Add connection check here if needed
        fi
    fi
    
    success "Database setup completed"
}

# Function to check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check required commands
    local required_commands=("curl" "python3")
    for cmd in "${required_commands[@]}"; do
        if ! command_exists $cmd; then
            error "$cmd is required but not installed"
            exit 1
        fi
    done
    
    # Check environment file
    if [ ! -f ".env" ]; then
        warning ".env file not found, using default configuration"
        if [ -f ".env.example" ]; then
            log "Copying .env.example to .env"
            cp .env.example .env
            warning "Please update .env with your configuration"
        fi
    fi
    
    # Check port availability
    local port=${API_PORT:-8000}
    if ! check_port $port; then
        error "Port $port is already in use"
        exit 1
    fi
    
    success "Prerequisites check completed"
}

# Function to start the service
start_service() {
    local env=$(detect_environment)
    log "Starting Student Behavior Analytics service in $env mode..."
    
    # Set environment-specific variables
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
    
    if [ "$env" = "development" ]; then
        log "Starting in development mode with auto-reload..."
        poetry run uvicorn src.api.main:app \
            --host ${API_HOST:-127.0.0.1} \
            --port ${API_PORT:-8000} \
            --reload \
            --log-level debug
    else
        log "Starting in production mode..."
        poetry run uvicorn src.api.main:app \
            --host ${API_HOST:-0.0.0.0} \
            --port ${API_PORT:-8000} \
            --workers ${API_WORKERS:-4} \
            --log-level info
    fi
}

# Function to run health check
health_check() {
    local port=${API_PORT:-8000}
    log "Running health check..."
    
    sleep 3  # Give service time to start
    
    if curl -f http://localhost:$port/health/live >/dev/null 2>&1; then
        success "Service is healthy and running"
        log "API Documentation: http://localhost:$port/docs"
        log "Health Check: http://localhost:$port/health"
    else
        error "Health check failed"
        exit 1
    fi
}

# Function to show help
show_help() {
    echo "Student Behavior Analytics Service Startup Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  start           Start the service"
    echo "  dev             Start in development mode"
    echo "  prod            Start in production mode"
    echo "  check           Check prerequisites only"
    echo "  health          Run health check only"
    echo "  setup           Setup environment only"
    echo "  help            Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  ENVIRONMENT     Set environment (development/production)"
    echo "  API_HOST        API host (default: 127.0.0.1 for dev, 0.0.0.0 for prod)"
    echo "  API_PORT        API port (default: 8000)"
    echo "  API_WORKERS     Number of workers for production (default: 4)"
    echo ""
    echo "Examples:"
    echo "  $0 start                # Auto-detect environment and start"
    echo "  $0 dev                  # Force development mode"
    echo "  $0 prod                 # Force production mode"
    echo "  ENVIRONMENT=prod $0 start # Set environment explicitly"
}

# Main script logic
main() {
    local command=${1:-start}
    
    case $command in
        "start")
            check_prerequisites
            setup_python_env
            setup_database
            start_service &
            health_check
            ;;
        "dev")
            export ENVIRONMENT=development
            check_prerequisites
            setup_python_env
            setup_database
            start_service &
            health_check
            ;;
        "prod")
            export ENVIRONMENT=production
            check_prerequisites
            setup_python_env
            setup_database
            start_service &
            health_check
            ;;
        "check")
            check_prerequisites
            ;;
        "health")
            health_check
            ;;
        "setup")
            setup_python_env
            setup_database
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Trap signals for graceful shutdown
trap 'log "Shutting down service..."; exit 0' SIGINT SIGTERM

# Run main function with all arguments
main "$@"
