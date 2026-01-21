````md
# ✅ Task Manager – FastAPI Full-Stack Application

A full-stack **Task Management** web application built using **FastAPI**, **SQLAlchemy**, and a simple **HTML + JavaScript UI**, deployed publicly on **Render (Free Tier)**.

This project demonstrates how to design, build, and deploy a **production-style backend system** with authentication, CRUD operations, pagination, and a frontend interface.

---

## 🚀 Live Demo (Public)

🔗 **https://task-manager-u2tm.onrender.com**

### ✅ Demo Credentials

```txt
Username: demo
Password: demo1234
````

> ℹ️ This project is deployed on Render Free Tier. The service may go to sleep after inactivity, and the database may reset on restarts.
> Demo user creation is handled automatically during startup for smooth usage.

---

## ✨ Features

### 🔐 Authentication & Security

* Login using username + password
* Password hashing using **Passlib** (stable on free deployment runtimes)
* Token-based authentication for protected routes
* User-level data isolation (each user sees only their own tasks)

### ✅ Task Management

* Create tasks
* View task list
* Update task title/description
* Mark task as completed / incomplete
* Delete tasks

### 📄 Scalable API Improvements

* Pagination support (`skip`, `limit`)
* Filtering (`completed=true/false`)
* Sorting (`sort=newest/oldest`)
* Proper response format with metadata:

  * total count
  * items array

### 🌍 Deployment

* Public deployment using **Render**
* Free-tier friendly demo setup
* Environment-variable based configuration using a central `settings.py`

---

## 🧰 Tech Stack

### Backend

* **FastAPI** (Python)
* **SQLAlchemy ORM**
* **SQLite** (default for demo)
* **JWT auth** using `python-jose`
* **Passlib** for password hashing

### Frontend

* HTML + CSS
* Vanilla JavaScript (Fetch API)
* Served directly from FastAPI

### Deployment

* Render (Free Tier)
* Uvicorn ASGI server
* `runtime.txt` used to pin Python version (optional but recommended)

---

## 🏗️ Project Structure

```bash
backend_task_manager/
├── app/
│   ├── main.py          # FastAPI app entry point + routes
│   ├── models.py        # SQLAlchemy DB models (User, Task)
│   ├── schemas.py       # Pydantic schemas (requests/responses)
│   ├── auth.py          # Auth, token creation, password hashing
│   ├── database.py      # DB engine + session setup
│   ├── settings.py      # Centralized environment-based config
│   ├── logger.py        # Logging configuration
│   └── __init__.py
├── templates/
│   └── index.html       # UI (Login + Task actions)
├── static/
│   └── styles.css       # Styling
├── requirements.txt     # Python dependencies
├── runtime.txt          # Python version pin (optional)
└── README.md
```

---

## 🔐 Authentication Flow (How Login Works)

1. User enters username & password in UI
2. UI calls `/auth/login`
3. Backend verifies user exists in DB
4. Password is verified using hashed password stored in DB
5. If valid, API returns an access token
6. UI stores token and uses it for authenticated endpoints:

   * `GET /tasks`
   * `POST /tasks`
   * `PATCH /tasks/{id}`
   * `DELETE /tasks/{id}`

---

## 🗄️ Database Design

### ✅ User Table

Stores authentication data.

| Column        | Type    | Notes           |
| ------------- | ------- | --------------- |
| id            | Integer | Primary Key     |
| username      | String  | Unique username |
| password_hash | String  | Hashed password |

### ✅ Task Table

Stores task data.

| Column      | Type    | Notes              |
| ----------- | ------- | ------------------ |
| id          | Integer | Primary Key        |
| title       | String  | Required           |
| description | String  | Optional           |
| completed   | Boolean | Default false      |
| owner_id    | Integer | Foreign key → User |

---

## 🔁 Demo User Auto-Creation (Free Hosting Friendly)

Because free cloud services can restart frequently, this project auto-creates a demo user at startup:

* Prevents login failure due to empty database
* Avoids requiring shell access (paid feature)
* Ensures the public demo is always usable

---

## 📌 API Endpoints

### ✅ Signup

Create a new user:

```http
POST /auth/signup
```

Payload:

```json
{
  "username": "yourname",
  "password": "yourpassword"
}
```

---

### ✅ Login

```http
POST /auth/login
```

Payload:

```json
{
  "username": "demo",
  "password": "demo1234"
}
```

Response:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

---

### ✅ List Tasks (Pagination + Filters)

```http
GET /tasks?skip=0&limit=20&completed=true&sort=newest
```

Response:

```json
{
  "total": 5,
  "skip": 0,
  "limit": 20,
  "items": [
    {
      "id": 10,
      "title": "Example",
      "description": "demo",
      "completed": false
    }
  ]
}
```

---

### ✅ Create Task

```http
POST /tasks
Authorization: Bearer <TOKEN>
```

Payload:

```json
{
  "title": "Buy groceries",
  "description": "Milk, fruits"
}
```

---

### ✅ Update Task

```http
PATCH /tasks/{task_id}
Authorization: Bearer <TOKEN>
```

Payload examples:

```json
{
  "completed": true
}
```

```json
{
  "title": "Updated title"
}
```

---

### ✅ Delete Task

```http
DELETE /tasks/{task_id}
Authorization: Bearer <TOKEN>
```

---

## ⚙️ Configuration (Environment Variables)

All configuration is managed via `app/settings.py`.

### Recommended Render Environment Variables

✅ Required:

```txt
SECRET_KEY=your-super-long-secret
```

Optional:

```txt
DATABASE_URL=sqlite:///./tasks.db
CREATE_DEMO_USER=true
DEMO_USERNAME=demo
DEMO_PASSWORD=demo1234
CORS_ORIGINS=*
```

---

## 🧪 Run Locally

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Start the server

```bash
uvicorn app.main:app --reload
```

### 3) Open in browser

```txt
http://127.0.0.1:8000
```

---

## 🛰️ Deploy on Render (Free Tier)

### Render Settings

* **Service Type:** Web Service
* **Root Directory:** `backend_task_manager`
* **Build Command:**

```bash
pip install -r requirements.txt
```

* **Start Command:**

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

> ⚠️ Render Free Tier may take 20–40 seconds to wake up after inactivity.

---

## 🧠 Interview Q&A (Most Common Questions)

### ✅ Why FastAPI?

FastAPI offers fast development, high performance, built-in validation, and clean API design.

### ✅ How is user isolation ensured?

Every query is scoped using `owner_id = current_user.id`, so users can only access their own tasks.

### ✅ How would you scale this?

* Replace SQLite with PostgreSQL
* Add caching (Redis)
* Add pagination (already implemented)
* Add monitoring/logging dashboards
* Add role-based access control

### ✅ What would you improve next?

* Add frontend improvements (task filters UI, load more)
* Add automated tests
* Add refresh tokens and token rotation
* Add Docker Compose + Postgres for local dev

---

## ✅ Key Takeaways

This project shows:

* Production-style backend architecture
* Authentication + authorization
* Database schema + ORM best practices
* Clean APIs with pagination & filters
* Public deployment on free infrastructure

---

## 📄 License

MIT

```
::contentReference[oaicite:0]{index=0}
```
