# Student Behavior Analytics - Frontend

Modern React-based frontend with Vite build system for the Student Behavior Analytics platform.

## Features

- **React 18** with modern hooks
- **Vite** for fast development and optimized production builds
- **Component Library** with reusable UI components
- **Error Boundaries** for graceful error handling
- **API Utilities** with retry logic and input sanitization
- **Constants** for magic number elimination
- **ESLint & Prettier** for code quality
- **TypeScript-ready** structure

## Installation

```bash
cd frontend
npm install
```

## Development

```bash
npm run dev
```

The dev server will run on `http://localhost:5173` with API proxy to `http://localhost:8000`.

## Build

```bash
npm run build
```

Builds the frontend to `../static/dist/` for production deployment.

## Linting

```bash
npm run lint
```

## Formatting

```bash
npm run format
```

## Component Library

Reusable components located in `src/components/`:

- **Navigation** - Shared navigation header
- **ErrorBoundary** - Error boundary for React components
- **Button** - Reusable button with variants
- **Card** - Card container with variants
- **LoadingSpinner** - Loading indicator
- **Toast** - Notification component

## Utilities

- `src/utils/api.js` - API utilities with retry logic and authentication
- `src/utils/constants.js` - Application constants

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable components
│   │   ├── Navigation.jsx
│   │   ├── ErrorBoundary.jsx
│   │   ├── Button.jsx
│   │   ├── Card.jsx
│   │   ├── LoadingSpinner.jsx
│   │   ├── Toast.jsx
│   │   └── index.js
│   └── utils/           # Utility functions
│       ├── api.js
│       └── constants.js
├── package.json
├── vite.config.js
├── .eslintrc.json
└── .prettierrc.json
```

## Migration from Templates

The existing HTML templates in `../templates/` can be gradually migrated to React components using this frontend structure. The component library provides a foundation for consistent UI across the application.

## API Integration

The frontend includes a comprehensive API utility module with:

- Automatic retry logic (3 retries by default)
- Input sanitization for XSS prevention
- Authentication token management
- Generic CRUD methods (GET, POST, PUT, DELETE)

Example usage:

```javascript
import { apiGet, apiPost, authenticatedRequest } from './utils/api';

// Simple GET request
const data = await apiGet('/students');

// Authenticated request
const result = await authenticatedRequest('POST', '/chat', { query: 'Analyze student S001' });
```
