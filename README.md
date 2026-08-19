# backstage-api-specs

This repository contains FastAPI services registered in the Backstage developer portal.

## APIs

| API | Description | Port |
|-----|-------------|------|
| [Products API](./products-api) | CRUD API for managing products | 8000 |
| [Football Results API](./football-results-api) | Fixtures, scores, teams and standings | 8001 |

## Backstage

Both APIs are registered in the Backstage catalog via [catalog-info.yaml](./catalog-info.yaml).
