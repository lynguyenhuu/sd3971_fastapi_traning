# To-dos APIs
- FastAPI
- Uvicorn
- SQL Alchemy
- Alembic

## First steps
- Change file name from .env.local to .env
- Update POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

## Start Docker Compose
```docker compose up```

## Init DB
Run
```alembic upgrade head```

### Default admin user
```
Username: admin
Password: 123456    
```
## API Docs
```http://localhost:8000/docs```