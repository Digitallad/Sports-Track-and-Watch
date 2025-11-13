# Rugby Atlas Backend API

**Rugby Atlas** is a global rugby broadcast rights, fixture intelligence, and user personalization platform. This backend API provides comprehensive data management and rights resolution for rugby matches worldwide.

## 🏉 Overview

Rugby Atlas helps rugby fans discover where to watch matches by:
- Managing fixture schedules for international and domestic competitions
- Resolving broadcast rights based on user location
- Providing intelligent personalization and notifications
- Ingesting data from multiple external sources

## 🚀 Features

- **Fixture Management**: Complete rugby match schedule database
- **Broadcast Rights Resolution**: Territory-based rights lookup with rules engine
- **Team & Competition Data**: Comprehensive rugby entity management
- **User Personalization**: Favorite teams, notifications, location-based customization
- **Data Ingestion**: Automated pipelines for external data sources
- **RESTful API**: Clean, documented FastAPI endpoints
- **Type Safety**: Full Pydantic validation and SQLAlchemy ORM
- **Database Migrations**: Alembic-based schema management

## 📋 Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Configuration**: Pydantic Settings
- **Containerization**: Docker + Docker Compose

## 🏗️ Project Structure

```
api/
├── src/
│   ├── core/              # Core infrastructure (config, db, logging)
│   ├── models/            # SQLAlchemy ORM models
│   ├── schemas/           # Pydantic request/response schemas
│   ├── routers/           # FastAPI route handlers
│   ├── services/          # Business logic layer
│   ├── ingestion/         # Data ingestion pipelines
│   ├── rights/            # Broadcast rights resolution engine
│   ├── utils/             # Utilities (timezone, text normalization, etc.)
│   └── tests/             # Test suite
├── alembic/               # Database migrations
├── Dockerfile
├── requirements.txt
└── alembic.ini
```

## 🛠️ Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL 16 (if running without Docker)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Sports-Track-and-Watch
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **Verify health**
   ```bash
   curl http://localhost:8000/health
   ```

5. **Access API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Local Development (without Docker)

1. **Create virtual environment**
   ```bash
   cd api
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database**
   ```bash
   # Ensure PostgreSQL is running
   createdb rugby_atlas
   ```

4. **Configure environment**
   ```bash
   export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/rugby_atlas"
   export ENVIRONMENT=development
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the server**
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 🗄️ Database Migrations

### Create a new migration
```bash
cd api
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

### View migration history
```bash
alembic history
```

## 🧪 Testing

Run the test suite:
```bash
cd api
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

## 📡 API Endpoints

### Health Check
- `GET /health` - Service health status
- `GET /healthz` - Kubernetes-style health check

### Core Resources
- `GET /api/v1/teams` - List teams
- `GET /api/v1/teams/{id}` - Get team details
- `GET /api/v1/competitions` - List competitions
- `GET /api/v1/fixtures` - List fixtures
- `GET /api/v1/fixtures/upcoming` - Upcoming fixtures
- `GET /api/v1/fixtures/team/{team_id}` - Team-specific fixtures

### Broadcast Rights
- `GET /api/v1/rights/fixture/{fixture_id}/territory/{territory_id}` - Resolve rights
- `GET /api/v1/rights/fixture/{fixture_id}` - All rights for fixture

### Users
- `GET /api/v1/users` - List users
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/{id}` - Get user details

See full API documentation at `/docs` when running the server.

## 🔧 Configuration

Key environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `ENVIRONMENT` | Environment (development/staging/production) | `development` |
| `DEBUG` | Enable debug mode | `true` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `API_PREFIX` | API route prefix | `/api/v1` |
| `SECRET_KEY` | Security secret | Required in production |

## 📊 Database Schema

### Core Entities
- **Sport**: Rugby Union, Rugby League, etc.
- **GoverningBody**: World Rugby, Six Nations, etc.
- **Competition**: Six Nations, Rugby Championship, etc.
- **Season**: Competition seasons
- **Team**: National teams, clubs
- **Venue**: Stadiums and arenas
- **Fixture**: Individual matches

### Broadcast Rights
- **Provider**: Broadcast companies (Sky, ESPN, etc.)
- **Platform**: Specific channels/apps
- **RightsPackage**: Rights agreements
- **FixtureRights**: Per-fixture, per-territory rights
- **Territory**: Geographic regions

### Users
- **User**: User accounts
- **UserLocation**: Location history
- **UserPreference**: Favorite teams/competitions
- **NotificationSubscription**: Notification settings

### Data Management
- **DataSource**: External data sources
- **IngestionJob**: Data ingestion tracking

## 🔄 Data Ingestion

The platform supports ingestion from multiple sources:

```python
from src.ingestion import FixturesIngestor, RightsIngestor

# Ingest fixtures
ingestor = FixturesIngestor(db)
results = ingestor.ingest_from_source(source_id=1, source_name="World Rugby")

# Ingest rights
rights_ingestor = RightsIngestor(db)
results = rights_ingestor.ingest_from_source(source_id=2, source_name="Provider API")
```

## 🎯 Rights Resolution

The rights resolution engine determines broadcast availability:

```python
from src.rights import RightsResolutionEngine

engine = RightsResolutionEngine(db)
rights = engine.resolve_for_fixture(
    fixture_id=123,
    territory_id=45,
    user_context={"subscriptions": ["sky_sports"]}
)
```

## 🛣️ Roadmap

### Phase 1: Foundation ✅
- Core data models
- API skeleton
- Rights resolution engine
- Database migrations

### Phase 2: Data Integration (In Progress)
- [ ] World Rugby API integration
- [ ] Six Nations data feed
- [ ] Provider rights ingestion
- [ ] Automated scheduling

### Phase 3: User Features
- [ ] Authentication & authorization
- [ ] User preferences API
- [ ] Notification system
- [ ] Personalized fixture feed

### Phase 4: Advanced Features
- [ ] GraphQL API
- [ ] Real-time updates (WebSockets)
- [ ] Caching layer (Redis)
- [ ] Search & filtering
- [ ] Admin dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is proprietary. All rights reserved.

## 👥 Authors

- Development Team - Rugby Atlas

## 📞 Support

For questions or support, please contact the development team.

---

**Built with ❤️ for rugby fans worldwide** 🏉
