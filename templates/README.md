# Templates

This directory contains HTML templates for the web application UI.

## Files

- **index.html** - Main landing page and student analysis dashboard
- **dashboard.html** - Comprehensive analytics dashboard
- **chat.html** - Conversational AI chat interface
- **api-builder.html** - API Builder for creating custom queries
- **agents.html** - AI agents interface
- **monitor.html** - System monitoring dashboard
- **docs.html** - Documentation viewer

## Features

- **Responsive Design**: Mobile-friendly UI with Tailwind CSS
- **Real-time Updates**: Live data fetching and display
- **Interactive Charts**: Data visualization with Chart.js
- **Role-based UI**: Different interfaces for different user roles
- **Dark Mode**: Modern dark theme design

## Usage

Templates are served by FastAPI using the `FileResponse` from the `templates/` directory:

```python
@app.get("/")
def root():
    return FileResponse("templates/index.html")
```

All templates include:
- Tailwind CSS for styling
- Chart.js for data visualization
- Fetch API for backend communication
- Responsive layout design
