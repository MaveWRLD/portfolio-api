# Portfolio API

Django REST API for backend developer portfolio case studies. Replaces Sanity CMS with a self-hosted solution that demonstrates backend engineering skills.

## Features

- **DRF ViewSets** with filtering, search, ordering
- **JWT Authentication** (access/refresh/blacklist) for admin endpoints
- **PostgreSQL** with UUID primary keys, indexes
- **Image uploads** to S3-compatible storage (R2, MinIO, AWS S3) or local
- **OpenAPI/Swagger** docs at `/api/docs/`
- **Django Admin** at `/admin/`
- **Health/readiness** endpoints for orchestration
- **Docker** multi-stage build for production
- **GitHub Actions** CI/CD pipeline

## Quick Start (Local)

```bash
# 1. Clone and enter
cd portfolio-api

# 2. Create env file
cp .env.example .env
# Edit .env with your values

# 3. Start with Docker Compose
docker compose up --build

# 4. Create superuser (in another terminal)
docker compose exec api python manage.py createsuperuser

# 5. Add content via /admin/ — content sections are singleton rows,
#    auto-created empty on first request; case studies are added manually
```

**Access:**
- API: http://localhost:8000/api/
- Swagger: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/
- Health: http://localhost:8000/api/health/
- MinIO Console: http://localhost:9001 (user: minioadmin, pass: minioadmin)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/case-studies/` | List case studies (paginated, filterable) |
| GET | `/api/case-studies/?featured=true` | Featured only |
| GET | `/api/case-studies/{slug}/` | Single case study detail |
| POST | `/api/case-studies/` | Create (admin only) |
| PATCH | `/api/case-studies/{slug}/` | Update (admin only) |
| DELETE | `/api/case-studies/{slug}/` | Delete (admin only) |
| POST | `/api/auth/token/` | Obtain JWT pair |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| POST | `/api/auth/token/blacklist/` | Blacklist refresh token |

## Frontend Integration

Replace Sanity fetch calls with direct API calls:

```typescript
// Before (Sanity)
const raw = await sanityClient.fetch(query)

// After (DRF)
const response = await fetch('/api/case-studies/')
const data = await response.json()
```

**Query params for list:**
- `featured=true|false`
- `category=Backend`
- `search=django`
- `ordering=-date` (or `date`, `title`, `created_at`)
- `page=2` (pagination)

## Deployment (Fly.io)

```bash
# 1. Install flyctl
curl -L https://fly.io/install.sh | sh

# 2. Launch (creates fly.toml, provisions Postgres)
fly launch --name portfolio-api --region iad --no-deploy

# 3. Set secrets
fly secrets set DJANGO_SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
fly secrets set POSTGRES_PASSWORD="$(openssl rand -base64 32)"
fly secrets set AWS_S3_ACCESS_KEY_ID=xxx AWS_S3_SECRET_ACCESS_KEY=xxx

# 4. Deploy
fly deploy

# 5. Run migrations, then add content via /admin/
fly ssh console -C "python manage.py migrate"
fly ssh console -C "python manage.py createsuperuser"
```

## Project Structure

```
portfolio-api/
├── config/                 # Django project settings
│   ├── settings/
│   │   ├── base.py        # Shared settings
│   │   ├── dev.py         # Development
│   │   ├── prod.py        # Production
│   │   └── test.py        # Testing
│   ├── urls.py            # Root URL config
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── core/              # Health checks, shared utilities
│   ├── case_studies/      # Case study models, APIs, admin
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── permissions.py
│   │   └── admin.py
│   └── content/            # Singleton page-section models (hero, brand,
│       │                   # contact, experience, projects, fun facts,
│       │                   # ticker, site settings) + read-only admin-edited API
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── admin.py
│       └── tests.py
├── media/                 # Local media (dev only)
├── staticfiles/           # Collected static (prod)
├── Dockerfile             # Multi-stage production build
├── docker-compose.yml     # Local development stack
├── pyproject.toml         # Dependencies & tool config
├── manage.py
└── .env.example
```

## Development Commands

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
pytest

# Lint & format
ruff check .
black .

# Collect static (production)
python manage.py collectstatic --noinput
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DJANGO_SECRET_KEY` | Yes | Django secret key |
| `DEBUG` | No | `True`/`False` (default: `True`) |
| `ALLOWED_HOSTS` | Yes | Comma-separated hosts |
| `CSRF_TRUSTED_ORIGINS` | No | Comma-separated origins for CSRF |
| `POSTGRES_*` | Yes | Database connection |
| `JWT_ACCESS_TTL` | No | Access token lifetime (default: `15m`) |
| `JWT_REFRESH_TTL` | No | Refresh token lifetime (default: `7d`) |
| `CORS_ALLOWED_ORIGINS` | No | Frontend origins |
| `AWS_S3_ENDPOINT_URL` | No | S3/MinIO endpoint (e.g. `http://minio:9000`) |
| `AWS_S3_ACCESS_KEY_ID` | No | Access key |
| `AWS_S3_SECRET_ACCESS_KEY` | No | Secret key |
| `AWS_STORAGE_BUCKET_NAME` | No | Bucket name |
| `AWS_S3_REGION_NAME` | No | Region (default: `us-east-1`) |

### MinIO (Local Development)

Docker Compose includes MinIO for S3-compatible local storage:

```bash
# MinIO API: http://localhost:9000
# MinIO Console: http://localhost:9001 (minioadmin / minioadmin)
# Bucket: portfolio-media (auto-created)
```

Media URLs in API responses will be: `http://localhost:9000/portfolio-media/case_studies/...`

## Why This Over Sanity?

| Aspect | Sanity | This API |
|--------|--------|----------|
| **Ownership** | SaaS vendor | You |
| **Schema** | Studio UI | Python models + migrations |
| **Auth** | Sanity's | Your JWT implementation |
| **Query** | GROQ | Django ORM + custom filters |
| **Deploy** | Two services | One container |
| **Cost** | Free tier limits | ~$5/mo (Fly.io hobby) |
| **Portfolio value** | "I used Sanity" | "I built this API" |

## License

MIT