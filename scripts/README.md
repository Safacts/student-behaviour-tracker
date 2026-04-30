# Scripts

This directory contains utility scripts and deployment files.

## Files

### Utility Scripts
- **data_generator.py** - Generate sample student activity data
- **db_importer.py** - Import data into the database
- **check_db.py** - Check database integrity
- **health_monitor.py** - Standalone health monitoring script
- **monitoring.py** - Application monitoring utilities
- **run_dashboard.py** - Run the dashboard standalone
- **api_service.py** - API service utilities

### Deployment Files
- **Dockerfile** - Docker container configuration
- **docker-compose.yml** - Docker Compose configuration
- **deploy.bat** - Windows deployment script
- **deploy.sh** - Linux/Mac deployment script
- **main_production.py** - Production entry point

## Usage

### Generate Sample Data
```bash
python scripts/data_generator.py
```

### Import Data
```bash
python scripts/db_importer.py
```

### Check Database
```bash
python scripts/check_db.py
```

### Deploy with Docker
```bash
docker-compose -f scripts/docker-compose.yml up
```

### Deploy on Windows
```bash
scripts\deploy.bat
```

### Deploy on Linux/Mac
```bash
bash scripts/deploy.sh
```
