# Ticketing System API

Back-end API for a support ticketing system (assessment project).

Built with Django, Django REST Framework, PostgreSQL, Celery, Redis, and Nginx via Docker Compose.

## Run locally with Docker

```bash
cp .env.example .env
docker compose up --build
```

API base URL: `http://localhost:8080`

Swagger UI: `http://localhost:8080/swagger/`

## Seed demo data

After the stack is running:

```bash
docker compose exec web python manage.py seed_demo
```

This creates:
- demo customer `customer1` (one order per status)
- demo admin `admin1`

The command prints their user ids.


## Time spent

| Area | Approx. time |
|------|--------------|
| Bootstrap (Docker, Nginx, Django/DRF) | 1.5 h |
| Data model + repositories | 2.5 h |
| User API + business rules | 2 h |
| Admin API | 1 h |
| Celery notifications | 1 h |
| Swagger + README | 0.5 h |
| **Total** | **~8.5 h** |

_Update the total above to reflect your actual time._
