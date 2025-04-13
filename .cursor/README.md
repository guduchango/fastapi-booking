# Cursor Development Rules

This document outlines the development rules and conventions for Python and FastAPI projects in Cursor.

## Python Conventions

### Import Order
1. Standard library imports
2. Third-party imports
3. Local application imports

### Naming Conventions
- Directories: lowercase_with_underscores
- Files: lowercase_with_underscores
- Variables: descriptive_with_auxiliary_verbs (e.g., is_active, has_permission)

### Function Conventions
- Use `def` for pure functions
- Use `async def` for asynchronous operations
- Type hints are required
- Early returns for error handling
- Guard clauses for preconditions

## FastAPI Conventions

### Route Definitions
- Use functional components
- Clear return type annotations
- Pydantic models for validation
- Async operations for I/O-bound tasks

### Error Handling
- Use HTTPException for expected errors
- Custom error types for consistency
- Proper error logging
- User-friendly error messages

### Performance Optimization
- Minimize blocking I/O
- Implement caching strategies
- Optimize serialization
- Use lazy loading

## File Structure
```
project/
├── routers/           # API route definitions
├── models/           # Database models
├── schemas/          # Pydantic models
├── utils/            # Utility functions
├── static/           # Static files
└── types/            # Type definitions
```

## Dependencies
Required packages:
- fastapi
- pydantic>=2.0.0
- sqlalchemy>=2.0.0
- asyncpg
- aiomysql

## Git Commit Messages
Format: `type(scope): description`
Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Test-related changes
- chore: Maintenance tasks

## Docker Configuration
Standard service configuration for API:
- Port: 8000
- Database URL: postgresql://admin:admin@postgres:5432/reservations

## Best Practices
1. Use functional, declarative programming
2. Avoid unnecessary classes
3. Prefer iteration and modularization
4. Use RORO (Receive an Object, Return an Object) pattern
5. Implement proper error handling and validation
6. Optimize for performance
7. Use middleware for cross-cutting concerns 