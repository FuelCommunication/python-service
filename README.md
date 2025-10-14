# Python service

Stack: litestar, pydantic, sqlalchemy[asyncpg], faststream[kafka], uv and ruff

## Running the service
### Locale

```bash
uv sync
litestar --app app.main:app run
```

```bash
docker build -t python-service .
docker run --rm python-service
```

# OpenAPI documentation
```
http://localhost:8000/schema (for ReDoc)
http://localhost:8000/schema/swagger (for Swagger UI)
http://localhost:8000/schema/elements (for Stoplight Elements)
http://localhost:8000/schema/rapidoc (for RapiDoc)
```

## License
This project is licensed under the **MIT License**.
