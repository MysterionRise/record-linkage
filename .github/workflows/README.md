# CI/CD Workflows

This directory contains GitHub Actions workflows for continuous integration and deployment.

## Workflows

### Backend CI (`backend-ci.yml`)
**Triggers:** Push to main/master/claude branches, PRs to main/master, changes to backend files

**Jobs:**
- **Test**: Runs tests on Python 3.12 and 3.13
  - Installs dependencies
  - Runs pytest with coverage
  - Uploads coverage to Codecov
- **Lint**: Code quality checks
  - Black formatting check
  - Flake8 linting
  - MyPy type checking
- **Security**: Security scanning
  - Safety (dependency vulnerabilities)
  - Bandit (security issues)

**Python Versions:**
- ✅ Python 3.12 (tested)
- ✅ Python 3.13 (tested)
- 🔜 Python 3.14 (will be added when released)

### Frontend CI (`frontend-ci.yml`)
**Triggers:** Push to main/master/claude branches, PRs to main/master, changes to frontend files

**Jobs:**
- **Test**: Build and validation
  - TypeScript type checking
  - ESLint validation
  - Production build
  - Unit tests (Vitest)
  - Uploads build artifacts
- **Lighthouse**: Performance audit (placeholder)

### Docker Build (`docker.yml`)
**Triggers:** Push to main/master/claude branches, PRs to main/master, changes to Docker files

**Jobs:**
- **build-backend**: Build and test backend Docker image
  - Uses Docker buildx
  - Tests health endpoint
  - Caches layers
- **build-frontend**: Build frontend Docker image
  - Uses Docker buildx
  - Caches layers
- **docker-compose**: Full stack test
  - Builds with docker-compose
  - Starts all services
  - Validates health endpoints
  - Tests integration

### Integration Tests (`integration.yml`)
**Triggers:** Push to main/master, PRs, nightly schedule (2 AM UTC)

**Jobs:**
- **integration**: Full stack integration test (30min timeout)
  - Starts services with docker-compose
  - Waits for services to be ready
  - Tests all API endpoints
  - Validates frontend accessibility
  - Collects logs on failure

## Running Locally

### Backend Tests
```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm install
npm test
npm run lint
npm run build
```

### Docker Tests
```bash
docker-compose build
docker-compose up -d
# Test endpoints
curl http://localhost:8000/api/v1/health
curl http://localhost:5173
docker-compose down
```

## Code Quality Standards

### Backend
- **Formatting**: Black (line length 100)
- **Linting**: Flake8
- **Type Checking**: MyPy
- **Testing**: Pytest with >80% coverage target
- **Security**: Bandit + Safety

### Frontend
- **Formatting**: Prettier (via ESLint)
- **Linting**: ESLint with TypeScript rules
- **Type Checking**: TypeScript strict mode
- **Testing**: Vitest

## Test Organization

### Backend Tests
- `test_api_*.py` - API endpoint tests
- `test_ml_*.py` - ML model and pipeline tests
- `conftest.py` - Shared fixtures
- Markers: `@pytest.mark.slow`, `@pytest.mark.integration`, `@pytest.mark.unit`

### Test Coverage
- Target: >80% code coverage
- Reports: Terminal, HTML, XML (for CI)
- Uploaded to Codecov for tracking

## Continuous Integration Strategy

1. **Fast Feedback**: Unit tests run on every push
2. **Multi-Python**: Test on Python 3.12 and 3.13
3. **Docker Validation**: Ensure containerized deployment works
4. **Integration Tests**: Full stack validation on PRs and nightly
5. **Security Scanning**: Automated vulnerability checks
6. **Code Quality**: Automated linting and formatting checks

## Adding New Tests

### Backend
```python
# tests/test_new_feature.py
import pytest

def test_new_feature(client):
    \"\"\"Test description.\"\"\"
    response = client.get("/api/v1/new-endpoint")
    assert response.status_code == 200
```

### Frontend
```typescript
// src/components/__tests__/NewComponent.test.tsx
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import NewComponent from '../NewComponent';

describe('NewComponent', () => {
  it('renders correctly', () => {
    const { getByText } = render(<NewComponent />);
    expect(getByText('Expected Text')).toBeInTheDocument();
  });
});
```

## Troubleshooting

### Backend CI Failures
- Check Python version compatibility
- Verify all dependencies are in requirements.txt
- Review test output in Actions logs
- Run locally: `pytest tests/ -v`

### Frontend CI Failures
- Check TypeScript errors: `npm run tsc --noEmit`
- Check linting: `npm run lint`
- Verify build: `npm run build`

### Docker CI Failures
- Check docker-compose.yml syntax
- Verify Dockerfiles
- Test locally with: `docker-compose up --build`

## Performance

### Current Benchmarks
- Backend tests: ~30-60 seconds (without slow tests)
- Frontend build: ~1-2 minutes
- Docker build (cached): ~2-3 minutes
- Integration tests: ~5-10 minutes

### Optimization
- Docker layer caching enabled
- npm/pip dependency caching
- Selective test execution based on file changes
