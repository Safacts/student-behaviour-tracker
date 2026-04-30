# Tests

This directory contains test files for the application.

## Test Files

- **test_ai_query_build.py** - Tests for AI-powered query building
- **test_api.py** - General API endpoint tests
- **test_api_builder_full.py** - API Builder integration tests
- **test_chat_api.py** - Chat API endpoint tests
- **test_chat_simple.py** - Simple chat functionality tests
- **test_compound_query.py** - Compound query handling tests
- **test_custom_query.py** - Custom query execution tests
- **test_greeting.py** - Greeting response tests
- **test_microservice_monitoring.py** - Health monitoring tests
- **test_mode_toggle.py** - LLM mode toggle tests
- **test_real_llm.py** - Real LLM integration tests
- **test_recommendation.py** - Recommendation system tests
- **test_report_apis.py** - Report generation API tests
- **test_report_endpoints.py** - Report endpoint tests
- **test_role_based_chat.py** - Role-based chat tests
- **test_v2_endpoints.py** - V2 API endpoint tests

## Test Structure

```
tests/
├── integration/  # Integration tests
├── performance/  # Performance tests
└── unit/         # Unit tests
```

## Running Tests

Run all tests:

```bash
python -m pytest tests/
```

Run specific test file:

```bash
python tests/test_chat_api.py
```

## Test Coverage

Tests cover:
- API endpoints
- Agent functionality
- Query building
- Chat functionality
- Health monitoring
- Role-based responses
- Workflow automation
