from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models, schemas, auth
from .database import SessionLocal
from .models import User
from .auth import get_password_hash
from fastapi import Query
from sqlalchemy import asc, desc

Base.metadata.create_all(bind=engine)

def create_demo_user():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "demo").first()
        if not user:
            demo = User(
                username="demo",
                password_hash=get_password_hash("demo123")
            )
            db.add(demo)
            db.commit()
            print("Demo user created")
    finally:
        db.close()

app = FastAPI(title="Task Manager API")
create_demo_user()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/auth/login", response_model=schemas.Token)
def login(form: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.username})
    return schemas.Token(access_token=token, token_type="bearer")


@app.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


@app.post("/tasks", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_task = models.Task(title=task.title, description=task.description or "", completed=False, owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks", response_model=schemas.TaskListResponse)
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    completed: bool | None = None,
    sort: str = Query("newest", pattern="^(newest|oldest)$"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    q = db.query(models.Task).filter(models.Task.owner_id == current_user.id)

    if completed is not None:
        q = q.filter(models.Task.completed == completed)

    total = q.count()

    if sort == "oldest":
        q = q.order_by(asc(models.Task.id))
    else:
        q = q.order_by(desc(models.Task.id))

    items = q.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items,
    }


@app.patch("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, patch: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if patch.title is not None:
        db_task.title = patch.title
    if patch.description is not None:
        db_task.description = patch.description
    if patch.completed is not None:
        db_task.completed = patch.completed
    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Deleted"}
