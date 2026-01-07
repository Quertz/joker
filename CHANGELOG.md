# Changelog

All notable changes to Joker API will be documented in this file.

## [2.1.0] - 2026-01-07

### 🌍 Globální Přístupnost

#### Changed
- **CORS Policy**: CORS je nyní plně otevřený (`origins: "*"`) pro maximální dostupnost
- Joker je záměrně veřejná služba pro PrintMastery z celého světa
- CORS je hardcoded v `app.py` a nelze konfigurovat přes environment variables
- Odstraněna konfigurace `CORS_ORIGINS` z `.env` (již není používána)
- Aktualizována dokumentace v README.md, DEPLOYMENT.md a config.py

#### Reasoning
- PrintMastery budou přistupovat z desítek různých domén po celém světě
- Není praktické ani možné udržovat whitelist všech originů
- Služba je již chráněna rate limitingem proti zneužití
- Veřejné API bez citlivých dat nepotřebuje CORS restrikce

## [2.0.0] - 2026-01-07

### 🚀 Production-Ready Release

Major overhaul transforming Joker into a production-ready standalone service for PrintMaster.

### ✨ Added

#### Security & Reliability
- **CORS Support**: Flask-CORS integration with configurable origins for PrintMaster integration
- **Rate Limiting**: Flask-Limiter with configurable limits to prevent abuse
- **Security Headers**: XSS, CSRF, Clickjacking protection headers on all responses
- **Comprehensive Logging**: Rotating file logs with configurable levels
- **Error Handlers**: Custom handlers for 404, 429, and 500 errors
- **Input Validation**: Enhanced validation for all user inputs

#### Performance
- **Caching System**: Pre-loading jokes into memory cache on startup
- **Optimized Loading**: Lazy loading with cache support for joke files
- **Health Checks**: Production-ready health endpoint with cache status

#### Configuration
- **Environment Variables**: Full .env support via python-dotenv
- **Config Module**: Centralized configuration (config.py) for different environments
- **Flexible Settings**: Configurable host, port, CORS origins, rate limits

#### DevOps & Deployment
- **Docker Support**:
  - Optimized Dockerfile with health checks
  - Docker Compose configuration
  - .dockerignore for efficient builds
- **CI/CD Pipeline**: GitHub Actions workflow with:
  - Multi-version Python testing (3.11, 3.12)
  - Code quality checks (black, flake8)
  - Docker build and test
  - Security scanning (bandit, safety)
- **Systemd Service**: Ready-to-use systemd service configuration

#### Documentation
- **DEPLOYMENT.md**: Comprehensive deployment guide for:
  - Docker deployment
  - Systemd service
  - Azure App Service
  - Kubernetes
  - Monitoring and troubleshooting
- **Updated README.md**: Production-focused documentation with:
  - Security best practices
  - Configuration examples
  - API documentation
  - Monitoring guides
- **CHANGELOG.md**: This file for tracking changes

#### New API Endpoints
- **GET /stats**: Returns statistics about available jokes per language and category
- Enhanced **/health**: Now includes cache status and version info
- Enhanced **/** (root): Now includes service info, rate limits, and examples

### 🔧 Changed

#### Dependencies
- Updated Flask: 3.0.0 → 3.1.0
- Updated Gunicorn: 21.2.0 → 22.0.0
- Added flask-cors: 5.0.0
- Added python-dotenv: 1.0.1
- Added Flask-Limiter: 3.8.0
- Added werkzeug: 3.1.3

#### Application Structure
- Refactored `app.py` with:
  - Modular structure
  - Better error handling
  - Comprehensive logging
  - Security middleware
  - Cache management
- Enhanced response format:
  - All responses now include `success` field
  - Added `timestamp` to responses
  - Added `service` identifier
  - Better error messages

#### API Responses
- **Standardized Format**: All successful responses include `success: true`
- **Error Details**: Error responses include both `error` and `message` fields
- **Metadata**: Responses include timestamps and service identifiers
- **Better Validation**: More descriptive validation error messages

### 📝 Infrastructure

#### Git & CI/CD
- Updated .gitignore for logs, .env files, and build artifacts
- Added GitHub Actions workflow (.github/workflows/ci-cd.yml)
- Added .dockerignore for optimized Docker builds

#### Configuration Files
- `.env.example`: Template for environment configuration
- `config.py`: Centralized configuration management
- `docker-compose.yml`: Production-ready Docker Compose setup
- `Dockerfile`: Optimized multi-stage build with health checks

### 🔒 Security Improvements

1. **CORS Protection**: Configurable allowed origins (no wildcards in production)
2. **Rate Limiting**: Per-endpoint limits to prevent abuse
3. **Security Headers**:
   - X-Content-Type-Options: nosniff
   - X-Frame-Options: DENY
   - X-XSS-Protection: 1; mode=block
   - Strict-Transport-Security
   - Content-Security-Policy
4. **Input Sanitization**: All inputs validated and sanitized
5. **Error Handling**: No sensitive information in error responses
6. **Logging**: Security events logged for audit

### 🎯 Breaking Changes

⚠️ **API Response Format Changes**:
- All successful responses now include `success: true` field
- Responses include `timestamp` field
- Error responses have new structure with `error` and `message` fields

**Migration Guide**:
```javascript
// Old response format (v1.0)
{
  "joke": "...",
  "language": "cz",
  "category": "normal"
}

// New response format (v2.0)
{
  "success": true,
  "joke": "...",
  "language": "cz",
  "category": "normal",
  "timestamp": "2026-01-07T10:30:00Z",
  "service": "Joker"
}
```

### 📊 Testing

- All endpoints tested and verified
- Error handling tested
- Health checks verified
- Rate limiting validated
- CORS functionality confirmed

### 🚀 Deployment Ready

The service is now production-ready with:
- ✅ Docker support
- ✅ Comprehensive logging
- ✅ Health monitoring
- ✅ Security hardening
- ✅ CI/CD pipeline
- ✅ Complete documentation
- ✅ Error handling
- ✅ Rate limiting
- ✅ CORS support

---

## [1.0.0] - 2024-XX-XX

### Initial Release
- Basic Flask application
- Support for 4 languages (cz, sk, en-gb, en-us)
- Support for 2 categories (normal, explicit)
- Simple REST API endpoints
- Azure App Service deployment support
