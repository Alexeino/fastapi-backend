# Hirestream.

This is the backend of the Full Stack Application Hirestream. This App uses following Tech Stack
-   FastAPI
-   PostgreSQL
-   OAuth2 with JWT Authentication
-   Redis for Cache

## Postgres Container
```bash
docker run --name hirestream-db -e POSTGRES_PASSWORD=db_password -e POSTGRES_USER=db_user -e POSTGRES_DB=database_name -p 5433:5432 -d postgres
```

## Features

### User Registeration

```bash
curl -X 'POST' \
  'http://localhost:8000/user/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string",
  "username": "string",
  "email": "user@example.com",
  "role": "CUSTOMER",
  "account_type": "RECRUITER",
  "password": "********"
}'

```