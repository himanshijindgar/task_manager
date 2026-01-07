# 🗂️ Task Manager — Full-Stack FastAPI Application

A production-style **Task Management web application** built using **FastAPI**, **SQLAlchemy**, and a lightweight **HTML + JavaScript frontend**, deployed publicly using **Render (Free Tier)**.

This project demonstrates **backend system design**, **authentication**, **data isolation**, **deployment**, and **real-world debugging** of Python web applications.

---

## 🌐 Live Demo (Public)

🔗 **https://task-manager-u2tm.onrender.com**

### Demo Credentials
Username: demo
Password: demo1234


> ℹ️ This project runs on free infrastructure. The demo database may reset if the instance restarts.

---

## 🎯 Why This Project Exists

This project was built to demonstrate:
- how real backend systems are structured
- how authentication & authorization work end-to-end
- how to deploy Python web applications publicly
- how to handle production-like issues (runtime versions, dependencies, auth edge cases)

It is **not a tutorial project** — it reflects **real engineering decisions** made under constraints (free hosting, no paid services).

---

## ✨ Features

- User authentication (token-based)
- Secure password hashing
- Create, read, update, delete (CRUD) tasks
- User-specific data isolation
- HTML UI served by backend
- RESTful API endpoints
- Public cloud deployment
- Auto-created demo user for free-tier stability

---

## 🧰 Tech Stack

### Backend
- **FastAPI** — high-performance Python web framework
- **SQLAlchemy** — ORM for database interaction
- **SQLite** — lightweight relational database
- **Passlib** — password hashing
- **Uvicorn** — ASGI server

### Frontend
- HTML
- CSS
- Vanilla JavaScript
- Fetch API for HTTP requests

### Deployment
- Render (Free Tier)
- Python 3.11 (runtime pinned for compatibility)

---

## 🏗️ Project Structure
backend_task_manager/
├── app/
│ ├── main.py # FastAPI app entry point
│ ├── models.py # Database models
│ ├── schemas.py # Request/response schemas
│ ├── auth.py # Authentication & hashing logic
│ ├── database.py # DB connection & session
│ └── init.py
├── templates/
│ └── index.html # Frontend UI
├── static/
│ └── styles.css
├── requirements.txt
├── runtime.txt # Python version pin
└── README.md

---

## 🔐 Authentication Design

### Flow
1. User submits username & password
2. Password is hashed & verified
3. Access token is generated
4. Token is required for protected endpoints
5. Each request validates the token before execution

### Why Token-Based Auth?
- Stateless
- Scales well
- No server-side session storage
- Standard practice in modern APIs

---

## 🔒 Password Hashing Strategy

This project uses **`sha256_crypt` via Passlib**.

### Why NOT bcrypt here?
- bcrypt requires native bindings
- bcrypt has compatibility issues with Python 3.13 on free cloud runtimes
- Free hosting environments restart often and cannot guarantee consistent native builds

### Why sha256_crypt is acceptable here
- Secure password hashing
- No native dependencies
- Stable across Python versions
- Suitable for demos & portfolios

> 🔐 In production systems, bcrypt or argon2 would be used with pinned runtimes.

---

## 🧪 Demo User Strategy (Free Tier Friendly)

Because free cloud services:
- restart containers
- reset ephemeral databases
- do not allow paid shell access

This app:
- automatically creates a **demo user on startup**
- avoids manual DB seeding
- ensures login always works for demos

This is a **common professional practice** for demo applications.

---

## 🗄️ Database Design

### Tables

#### User
| Field | Type | Description |
|------|------|-------------|
| id | int | Primary key |
| username | string | Unique |
| password_hash | string | Hashed password |

#### Task
| Field | Type | Description |
|------|------|-------------|
| id | int | Primary key |
| title | string | Task title |
| description | string | Optional |
| completed | boolean | Status |
| owner_id | int | FK → User |

---

## 🔐 Data Isolation

- Each task is linked to a user
- Queries always filter by authenticated user
- Users cannot view or modify other users’ tasks

This mimics **multi-tenant application design**.

---

## 🚀 Deployment Details

- Deployed on **Render (Free Tier)**
- Uses **Uvicorn** as ASGI server
- Python runtime pinned using `runtime.txt`
- Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT


---

## 🧠 Common Interview Questions (Answered)

### Why FastAPI?
FastAPI provides:
- async support
- high performance
- automatic validation
- clean API design

---

### Why SQLite?
- Zero configuration
- Ideal for demos
- Easily replaceable with PostgreSQL

---

### How would you scale this?
- Replace SQLite with PostgreSQL
- Add Redis caching
- Introduce pagination
- Add role-based access
- Deploy behind a load balancer

---

### How is security handled?
- Passwords are hashed
- Tokens expire
- User-scoped data access
- No plaintext secrets stored

---

### Why deploy on free infrastructure?
To demonstrate:
- cost-conscious engineering
- ability to work under constraints
- real deployment & debugging skills

---

## 🧪 Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
Visit: http://127.0.0.1:8000
