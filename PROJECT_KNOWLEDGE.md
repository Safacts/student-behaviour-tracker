# Student Behavior Analytics - Complete Project Knowledge

## Project Overview
This is a production-grade microservice for analyzing student behavior patterns, identifying at-risk students, and providing AI-powered recommendations for parents and educators.

## Architecture
- **Framework**: FastAPI (Python 3.11)
- **Database**: SQLite (behavior.db)
- **AI Integration**: OpenAI GPT-3.5 API with rule-based fallback
- **Deployment**: Docker containerized with docker-compose

## Core Components

### Main Application (main.py)
- FastAPI application running on port 8000
- RESTful API endpoints for students, activity logs, reports, and agents
- Integrated with production-grade middleware and monitoring

### Analysis Components
- **analyzer.py**: Student behavior analysis logic
- **llm_service.py**: AI-powered parent report generation with OpenAI API
- **hybrid approach**: Uses AI when available, falls back to heuristic rules

### Production-Grade Features (All Implemented)

#### 1. Structured Logging System (logger.py)
- File and console logging with configurable levels
- Structured JSON logging for API requests and agent executions
- Automatic log rotation and timestamping
- Separate loggers: main, api, agents, database

#### 2. Health Monitoring System (health_monitor.py)
- System metrics collection (uptime, database size, response times)
- Database integrity checks
- AI service health monitoring
- Metrics history and trend analysis
- Comprehensive health summary endpoint

#### 3. API Rate Limiting (rate_limiter.py)
- Configurable rate limiting per client IP
- Time-window based throttling
- Statistics tracking (hits, misses, remaining)
- Graceful handling of rate limit exceeded scenarios

#### 4. Authentication Hooks (auth.py)
- API key generation and validation
- Token-based authentication with expiration
- Password hashing and verification
- Session management
- User authentication statistics

#### 5. Caching System (cache.py)
- In-memory caching with TTL support
- Cache statistics (hit rate, memory usage)
- Automatic cleanup of expired entries
- Performance optimization for frequently accessed data

#### 6. Real-time WebSocket Updates (websocket_manager.py)
- WebSocket connection management
- Client grouping and targeted messaging
- Connection statistics and monitoring
- Broadcast and personal message support

#### 7. Production Deployment Configuration
- **Dockerfile**: Multi-stage Docker build for production
- **docker-compose.yml**: Complete orchestration with Nginx proxy
- **.env.production**: Production environment variables
- **deploy.sh/deploy.bat**: Deployment scripts for Linux/Windows
- Health checks and automatic restart policies

#### 8. Advanced Data Validation (validators.py)
- Multi-level validation (strict, moderate, lenient)
- Student ID, name, marks, and data validation
- Input sanitization for security
- Comprehensive error reporting

#### 9. Comprehensive Testing Suite (test_api.py)
- API endpoint testing
- Data validation testing
- Cache system testing
- Authentication testing
- Health monitoring testing
- Rate limiting testing

## API Endpoints

### Core Endpoints
- **GET /api/students** - List all students (with caching, rate limiting)
- **GET /api/activity-logs** - Get all activity logs (with rate limiting)
- **GET /api/report/{student_id}** - Generate student report (with validation, caching, rate limiting)
- **GET /api/agents** - List available AI agents

### Health Monitoring Endpoints
- **GET /api/health** - Basic health status
- **GET /api/health/detailed** - Detailed health metrics
- **GET /api/health/metrics** - Metrics history and trends

### Web Interfaces
- **GET /** - Main dashboard
- **GET /dashboard** - Testing dashboard
- **GET /agents** - Agents interface
- **GET /monitor** - System monitor
- **GET /docs** - API documentation

## Database Schema
- **student_activity table**: 
  - id (primary key)
  - student_id (student identifier)
  - student_name (student name)
  - date (activity date)
  - time_spent_mins (study time in minutes)
  - distraction_score (0-10 scale)
  - marks_achieved_percent (0-100 percentage)

## AI/Heuristic System Details

### AI Component (OpenAI GPT-3.5)
- Used when OPENAI_API_KEY is available and valid
- Generates empathetic, context-aware parent recommendations
- 3-sentence format with emotional intelligence
- Configurable temperature and token limits

### Heuristic Component (Rule-based)
- Activates when AI API is unavailable or fails
- Predefined rules based on behavioral tags:
  - "High Flight Risk" - Academic challenges, high distraction
  - "Concept Comprehension Issue" - Good effort but different learning approaches needed
  - "On Track" - Good progress, positive trajectory
- Consistent, reliable fallback responses

## Behavioral Analysis Tags
- **High Flight Risk**: Low marks (<50%) and/or high distraction (>6)
- **Concept Comprehension Issue**: Low marks (<70%) but low distraction (<3)
- **On Track**: Good marks (>70%) and reasonable distraction
- **High Performer**: Excellent marks (>85%) with good habits

## Current Issues
- Service startup issues after integrating production-grade features
- Import errors in main.py when using all production-grade components
- Need to resolve integration conflicts between new components

## File Structure
```
student_behavior_analysis/
├── main.py                      # Main FastAPI application
├── analyzer.py                  # Student behavior analysis
├── llm_service.py              # AI-powered report generation
├── behavior.db                 # SQLite database
├── logger.py                   # Structured logging system
├── health_monitor.py          # Health monitoring system
├── rate_limiter.py            # API rate limiting
├── auth.py                    # Authentication system
├── cache.py                   # Caching system
├── websocket_manager.py       # WebSocket management
├── validators.py              # Data validation
├── test_api.py                # Testing suite
├── Dockerfile                 # Production Docker image
├── docker-compose.yml         # Docker orchestration
├── .env.production            # Production environment
├── deploy.sh                  # Linux deployment script
├── deploy.bat                 # Windows deployment script
├── index.html                 # Main web interface
├── dashboard.html             # Dashboard interface
├── agents.html                # Agents interface
├── monitor.html               # System monitor
├── docs.html                  # Documentation
├── logs/                      # Log files directory
└── requirements.txt           # Python dependencies
```

## Dependencies
- fastapi
- uvicorn
- openai
- python-dotenv
- sqlite3 (built-in)
- Standard Python libraries (logging, json, time, etc.)

## Environment Variables
- OPENAI_API_KEY - OpenAI API key for AI recommendations
- DATABASE_URL - Database connection string
- LOG_LEVEL - Logging level (INFO, DEBUG, etc.)
- RATE_LIMIT_MAX_REQUESTS - Rate limit threshold
- RATE_LIMIT_WINDOW_SECONDS - Rate limit time window
- AUTH_SECRET_KEY - Authentication secret key
- CORS_ORIGINS - Allowed CORS origins
- HOST - Server host address
- PORT - Server port
- WORKERS - Number of worker processes

## Security Features
- CORS middleware
- Security headers (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection)
- Input validation and sanitization
- API key authentication
- Token-based authentication with expiration
- Password hashing
- Rate limiting to prevent abuse

## Performance Optimizations
- In-memory caching with TTL
- Database connection pooling
- Rate limiting to prevent overload
- Efficient database queries
- Response time tracking
- Cache hit rate monitoring

## Monitoring Capabilities
- System metrics (uptime, database size, response times)
- Database integrity checks
- AI service health monitoring
- API request logging and tracking
- Agent execution monitoring
- Cache statistics
- Rate limiting statistics
- Authentication statistics

## Deployment Strategy
- Docker containerization for consistency
- Multi-stage Docker builds for optimization
- Docker Compose for orchestration
- Nginx reverse proxy for load balancing
- Health checks for automatic recovery
- Environment-based configuration
- Production deployment scripts

## Testing Strategy
- API endpoint testing
- Component unit testing
- Integration testing
- Health monitoring testing
- Performance testing
- Security testing
- Rate limiting validation

## Known Limitations
- SQLite database not suitable for high-concurrency production
- In-memory cache not persistent across restarts
- WebSocket manager is simplified (not production-ready for real-time features)
- Authentication system uses in-memory storage (not suitable for production)
- Rate limiting is per-process (not distributed)

## Future Enhancements
- PostgreSQL for production database
- Redis for distributed caching
- Production-ready WebSocket implementation
- JWT-based authentication with database backing
- Distributed rate limiting with Redis
- Enhanced monitoring with Prometheus/Grafana
- CI/CD pipeline integration
- Advanced security features (CSRF protection, etc.)

## Integration Notes
- All production-grade features are implemented as standalone modules
- Integration into main.py requires careful dependency management
- Some components have circular dependency risks
- Need to resolve import conflicts for full integration
- Current service works without production-grade features integrated

## Git Repository Status
- Repository needs to be initialized
- All production-grade components ready for commit
- Main application needs to be fixed for production integration
- Deployment configuration files ready
- Documentation complete
