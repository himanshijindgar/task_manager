# Task Manager Backend (FastAPI + HTML UI)

A senior-level sample project:

- FastAPI backend
- JWT-style auth
- SQLite (can be swapped to Postgres)
- Simple HTML+JS frontend using Fetch API
- Dockerfile included

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open: http://127.0.0.1:8000

### Create demo user

```python
from app.database import SessionLocal, Base, engine
from app import models, auth
Base.metadata.create_all(bind=engine)
db = SessionLocal()
user = models.User(username="demo", password_hash=auth.get_password_hash("demo123"))
db.add(user)
db.commit()
db.close()
```

Login with:
- username: demo
- password: demo123

## Deploy (Render / Railway)

- Build from this repo
- Use the Dockerfile
- Expose port 8000
