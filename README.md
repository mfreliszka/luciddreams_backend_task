# Lucid Dreams Backend Task

## Project Description

This is a FastAPI web application following the MVC (Model-View-Controller) design pattern. It includes:

- FastAPI as the web framework

- MySQL as the database (via Docker Compose)

- Redis for caching

- JWT Authentication for secure user access

- Alembic for database migrations

- Poetry for dependency management

## Requirements

- Python 3.8+
- Virtualenv
- PostgreSQL (or another compatible database)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/luciddreams_backend_task.git
   cd luciddreams_backend_task
   ```

2. Create ``.env`` file:

   ```
   DATABASE_URL=mysql+mysqlconnector://user:password@db/fastapi_db
    SECRET_KEY=SUPERSECRETJWTKEY
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    REDIS_HOST=redis
    REDIS_PORT=6379
   ```

3. Start Docker Services:

   ```docker-compose up -d --build```

4. Apply Database Migrations:

   ``docker exec -it fastapi_app alembic upgrade head``

5. Test API

   ``curl http://localhost:8000``
