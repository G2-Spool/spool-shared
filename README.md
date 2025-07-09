# Spool Shared Library

Common utilities and shared code for Spool microservices.

**Status:** ✅ Deployed to CodeBuild

## Features

- **Authentication**: JWT token validation utilities
- **Database**: Common database models and utilities
- **Schemas**: Shared Pydantic schemas
- **Middleware**: Common FastAPI middleware
- **Utils**: General utility functions
- **Exceptions**: Common exception classes
- **Constants**: Shared constants and enums

## Installation

```bash
pip install git+https://github.com/G2-Spool/spool-shared.git
```

## Usage

```python
from spool_shared.auth import decode_jwt_token
from spool_shared.schemas.common import PaginationParams
from spool_shared.exceptions import SpoolException
from spool_shared.utils.validators import validate_uuid

# JWT validation
token_data = decode_jwt_token(token)

# Pagination
params = PaginationParams(page=1, size=20)

# Error handling
raise SpoolException(
    status_code=400,
    detail="Invalid request"
)
```

## Development

```bash
# Install in development mode
pip install -e .

# Run tests
pytest tests/

# Format code
black spool_shared/
isort spool_shared/
```

## Structure

```
spool_shared/
├── auth/           # Authentication utilities
├── database/       # Database utilities
├── schemas/        # Shared Pydantic schemas
├── middleware/     # FastAPI middleware
├── utils/          # General utilities
├── exceptions/     # Exception classes
└── constants/      # Constants and enums
```