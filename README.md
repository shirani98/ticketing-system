# Ticketing System API

Back-end API for a support ticketing system (assessment project).

## Run locally with Docker

```bash
cp .env.example .env
docker compose up --build
```

## Seed demo data

After the stack is running, load sample customer and orders:

```bash
docker compose exec web python manage.py seed_demo
```

This creates a demo customer (`customer1`) with one order per status. The command prints the customer id to use with optional `X-User-Id` header.

## Notes

- Nginx proxies all requests to the Django app.
- Swagger UI: `http://localhost:8080/swagger/`
