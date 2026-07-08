# Ticketing System API

Back-end API for a support ticketing system (assessment project).

## Run locally with Docker

```bash
cp .env.example .env
docker compose up --build
```

## Notes

- Nginx proxies all requests to the Django app.
