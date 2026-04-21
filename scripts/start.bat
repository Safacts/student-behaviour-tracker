@echo off
REM Student Behavior Analytics Service Startup Script for Windows
REM This script handles environment setup and service startup

setlocal enabledelayedexpansion

REM Colors for output (limited support in Windows)
set "INFO=[INFO]"
set "ERROR=[ERROR]"
set "SUCCESS=[SUCCESS]"
set "WARNING=[WARNING]"

REM Logging function
:log
echo %INFO% %date% %time% %~1
goto :eof

:error
echo %ERROR% %~1
goto :eof

:success
echo %SUCCESS% %~1
goto :eof

:warning
echo %WARNING% %~1
goto :eof

REM Function to check if command exists
:command_exists
where %1 >nul 2>&1
goto :eof

REM Function to detect environment
:detect_environment
if defined ENVIRONMENT (
    echo !ENVIRONMENT!
) else (
    if exist ".env" (
        findstr /C:"ENVIRONMENT=production" .env >nul 2>&1
        if !errorlevel! equ 0 (
            echo production
        ) else (
            echo development
        )
    ) else (
        echo development
    )
)
goto :eof

REM Function to setup Python environment
:setup_python_env
call :log "Setting up Python environment..."

call :command_exists python
if !errorlevel! neq 0 (
    call :error "Python is required but not installed"
    exit /b 1
)

call :command_exists poetry
if !errorlevel! neq 0 (
    call :log "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python -
    set "PATH=%USERPROFILE%\.local\bin;%PATH%"
)

if exist "pyproject.toml" (
    call :log "Installing dependencies with Poetry..."
    poetry install
    if !errorlevel! neq 0 (
        call :error "Failed to install dependencies"
        exit /b 1
    )
) else (
    call :error "pyproject.toml not found"
    exit /b 1
)

call :success "Python environment setup completed"
goto :eof

REM Function to setup database
:setup_database
call :log "Setting up database..."

REM Create data directory
if not exist "data" mkdir data
if not exist "logs" mkdir logs

call :detect_environment
set "env=!errorlevel!"

if "!env!"=="development" (
    call :log "Using SQLite database for development"
) else (
    call :log "Using PostgreSQL for production"
)

call :success "Database setup completed"
goto :eof

REM Function to check prerequisites
:check_prerequisites
call :log "Checking prerequisites..."

REM Check required commands
call :command_exists python
if !errorlevel! neq 0 (
    call :error "Python is required but not installed"
    exit /b 1
)

call :command_exists curl
if !errorlevel! neq 0 (
    call :error "curl is required but not installed"
    exit /b 1
)

REM Check environment file
if not exist ".env" (
    call :warning ".env file not found, using default configuration"
    if exist ".env.example" (
        call :log "Copying .env.example to .env"
        copy .env.example .env >nul
        call :warning "Please update .env with your configuration"
    )
)

call :success "Prerequisites check completed"
goto :eof

REM Function to start the service
:start_service
call :detect_environment
set "env=!errorlevel!"

call :log "Starting Student Behavior Analytics service in !env! mode..."

REM Set environment-specific variables
set "PYTHONPATH=%PYTHONPATH%;%cd%\src"

if "!env!"=="development" (
    call :log "Starting in development mode with auto-reload..."
    poetry run uvicorn src.api.main:app --host %API_HOST% --port %API_PORT% --reload --log-level debug
) else (
    call :log "Starting in production mode..."
    poetry run uvicorn src.api.main:app --host %API_HOST% --port %API_PORT% --workers %API_WORKERS% --log-level info
)
goto :eof

REM Function to run health check
:health_check
call :log "Running health check..."

timeout /t 3 /nobreak >nul

set "port=%API_PORT%"
if "%API_PORT%"=="" set "port=8000"

curl -f http://localhost:%port%/health/live >nul 2>&1
if !errorlevel! equ 0 (
    call :success "Service is healthy and running"
    call :log "API Documentation: http://localhost:%port%/docs"
    call :log "Health Check: http://localhost:%port%/health"
) else (
    call :error "Health check failed"
    exit /b 1
)
goto :eof

REM Function to show help
:show_help
echo Student Behavior Analytics Service Startup Script
echo.
echo Usage: %0 [OPTIONS]
echo.
echo Options:
echo   start           Start the service
echo   dev             Start in development mode
echo   prod            Start in production mode
echo   check           Check prerequisites only
echo   health          Run health check only
echo   setup           Setup environment only
echo   help            Show this help message
echo.
echo Environment Variables:
echo   ENVIRONMENT     Set environment (development/production)
echo   API_HOST        API host (default: 127.0.0.1 for dev, 0.0.0.0 for prod)
echo   API_PORT        API port (default: 8000)
echo   API_WORKERS     Number of workers for production (default: 4)
echo.
echo Examples:
echo   %0 start                # Auto-detect environment and start
echo   %0 dev                  # Force development mode
echo   %0 prod                 # Force production mode
echo   set ENVIRONMENT=prod ^&^& %0 start # Set environment explicitly
goto :eof

REM Main script logic
:main
set "command=%1"
if "%command%"=="" set "command=start"

REM Set default values
if "%API_HOST%"=="" (
    if "%ENVIRONMENT%"=="production" (
        set "API_HOST=0.0.0.0"
    ) else (
        set "API_HOST=127.0.0.1"
    )
)

if "%API_PORT%"=="" set "API_PORT=8000"
if "%API_WORKERS%"=="" set "API_WORKERS=4"

if "%command%"=="start" (
    call :check_prerequisites
    if !errorlevel! neq 0 exit /b 1
    call :setup_python_env
    if !errorlevel! neq 0 exit /b 1
    call :setup_database
    if !errorlevel! neq 0 exit /b 1
    call :start_service
    call :health_check
) else if "%command%"=="dev" (
    set "ENVIRONMENT=development"
    call :check_prerequisites
    if !errorlevel! neq 0 exit /b 1
    call :setup_python_env
    if !errorlevel! neq 0 exit /b 1
    call :setup_database
    if !errorlevel! neq 0 exit /b 1
    call :start_service
    call :health_check
) else if "%command%"=="prod" (
    set "ENVIRONMENT=production"
    call :check_prerequisites
    if !errorlevel! neq 0 exit /b 1
    call :setup_python_env
    if !errorlevel! neq 0 exit /b 1
    call :setup_database
    if !errorlevel! neq 0 exit /b 1
    call :start_service
    call :health_check
) else if "%command%"=="check" (
    call :check_prerequisites
) else if "%command%"=="health" (
    call :health_check
) else if "%command%"=="setup" (
    call :setup_python_env
    if !errorlevel! neq 0 exit /b 1
    call :setup_database
) else if "%command%"=="help" (
    call :show_help
) else (
    call :error "Unknown command: %command%"
    call :show_help
    exit /b 1
)

goto :eof

REM Call main function with all arguments
call :main %*
