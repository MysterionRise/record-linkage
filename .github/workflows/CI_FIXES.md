# CI/CD Issues Analysis and Fixes

## Issues Identified

### 1. ❌ Python 3.13 Compatibility
**Problem**: Python 3.13 was in the test matrix, but ML libraries (PyTorch, transformers, sentence-transformers) don't have pre-built wheels for 3.13 yet.

**Impact**: Backend CI would fail during dependency installation.

**Fix**: Temporarily disabled Python 3.13 testing. Using only Python 3.12 until ML libraries release 3.13-compatible wheels.

```yaml
matrix:
  python-version: ['3.12']
  # Python 3.13 temporarily disabled - ML libraries don't have wheels yet
```

### 2. ❌ Missing package-lock.json
**Problem**: Frontend workflow used `npm ci` which requires `package-lock.json`, but we never generated this file.

**Impact**: Frontend CI would fail immediately on npm install step.

**Fix**: Changed to `npm install` and updated cache path to `frontend/package.json`.

```yaml
- name: Install dependencies
  working-directory: ./frontend
  run: npm install  # Changed from npm ci
```

### 3. ❌ Docker Compose Command
**Problem**: Workflows used old `docker-compose` command. Modern Docker (v2+) uses `docker compose` (space, not hyphen).

**Impact**: Docker workflows would fail with "command not found" on GitHub Actions runners.

**Fix**: Updated all instances to `docker compose`.

```yaml
run: docker compose build
run: docker compose up -d
run: docker compose down
```

### 4. ⚠️ Missing pip Cache Dependency Path
**Problem**: Backend CI specified `cache: 'pip'` without `cache-dependency-path`.

**Impact**: Caching might not work optimally or could fail.

**Fix**: Added explicit cache path.

```yaml
cache: 'pip'
cache-dependency-path: backend/requirements.txt
```

### 5. ⚠️ Codecov Action Version
**Problem**: Using `codecov/codecov-action@v3` which may be outdated.

**Status**: Left as-is for now (v3 is still supported), but should monitor for v4 release.

## Files Modified

1. `.github/workflows/backend-ci.yml`
   - Removed Python 3.13 from matrix
   - Added cache-dependency-path for all Python setup steps

2. `.github/workflows/frontend-ci.yml`
   - Changed `npm ci` to `npm install`
   - Changed cache path from package-lock.json to package.json

3. `.github/workflows/docker.yml`
   - Changed all `docker-compose` to `docker compose`

4. `.github/workflows/integration.yml`
   - Changed all `docker-compose` to `docker compose`

## Expected Results After Fixes

### Backend CI
- ✅ Tests will run on Python 3.12
- ✅ Dependencies will install successfully
- ✅ Linting and security scans will complete
- ✅ Coverage reports will upload to Codecov

### Frontend CI
- ✅ Dependencies will install without package-lock.json
- ✅ TypeScript type checking will run
- ✅ Build will complete successfully
- ✅ Artifacts will upload correctly (v4)

### Docker Workflows
- ✅ Images will build successfully
- ✅ docker compose commands will execute
- ✅ Health checks will pass
- ✅ Integration tests will complete

## Future Improvements

1. **Python 3.13 Support**: Re-enable when ML libraries add support (likely Q1-Q2 2025)
   - Monitor PyTorch, transformers, sentence-transformers releases
   - Add back to matrix: `python-version: ['3.12', '3.13']`

2. **Generate package-lock.json**: For more deterministic frontend builds
   ```bash
   cd frontend && npm install  # Generates package-lock.json
   git add frontend/package-lock.json
   ```
   Then switch back to `npm ci` in workflow

3. **Python 3.14 Support**: Add when released (expected late 2025)

4. **Upgrade Codecov Action**: Monitor for v4 release

## Testing Locally

Before pushing, test workflows locally:

```bash
# Backend tests
cd backend
python3.12 -m pip install -r requirements.txt
pytest tests/ -v

# Frontend build
cd frontend
npm install
npm run build
npm run lint

# Docker
docker compose build
docker compose up -d
docker compose down
```
