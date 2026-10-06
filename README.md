# User Product API

A REST API built with **FastAPI** for user registration and authentication, product management, and authenticated file uploads. The application uses **SQLAlchemy with PostgreSQL**, **JWT bearer authentication**, **role-based authorization**, **request/response middleware logging**, and **rate limiting**.

## Features

* User registration and authentication
* JWT bearer token authentication
* User profile and user-list endpoints
* Product CRUD operations
* Role-based authorization
* Admin-only product deletion
* Authenticated file uploads
* PostgreSQL database integration
* SQLAlchemy ORM
* Request/response logging middleware
* Request execution-time logging
* Rate limiting for authentication endpoints
* Interactive Swagger/OpenAPI documentation
* ReDoc API documentation
* Docker and Docker Compose support
* Pytest API tests

## Technologies

* Python 3.12+
* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT
* Pydantic
* Uvicorn
* SlowAPI
* Pytest
* Docker
* Docker Compose

---

# Middleware Logging

The application includes custom **HTTP middleware** for request and response logging.

The middleware runs for every incoming HTTP request.

It records information such as:

* HTTP method
* Request path
* Response status code
* Request execution time

Example log:

```text
INFO: REQUEST: POST /auth/login
INFO: RESPONSE: POST /auth/login - 200 - 0.142s
```

For another request:

```text
INFO: REQUEST: GET /products/
INFO: RESPONSE: GET /products/ - 200 - 0.038s
```

This makes it easier to monitor API behavior and identify slow endpoints.

### Middleware Flow

```text
Client
  |
  v
HTTP Request
  |
  v
Logging Middleware
  |
  v
FastAPI Router
  |
  v
Endpoint
  |
  v
Response
  |
  v
Logging Middleware
  |
  v
Client
```

The middleware measures the time between receiving the request and returning the response.

Conceptually:

```text
start_time = current time

process request

execution_time = current time - start_time
```

The execution time is logged along with the response status.

---

# Rate Limiting

The API uses **SlowAPI** to protect endpoints from excessive requests.

Rate limiting controls how frequently a client can call a particular endpoint within a specified time period.

The login endpoint is limited to:

```text
3 requests per minute
```

This helps reduce excessive authentication attempts and provides basic protection against repeated login requests.

### Login Rate-Limit Example

```text
Request 1 → /auth/login → Allowed
Request 2 → /auth/login → Allowed
Request 3 → /auth/login → Allowed
Request 4 → /auth/login → Rate limited
```

A client exceeding the configured limit receives a rate-limit response instead of the request being processed normally.

### Why Rate Limiting Is Used

Without rate limiting:

```text
Client
  |
  | Login request
  | Login request
  | Login request
  | Login request
  | Login request
  v
FastAPI
```

A client could repeatedly call the login endpoint.

With rate limiting:

```text
Client
  |
  v
Rate Limiter
  |
  +---- Within limit ----> FastAPI
  |
  +---- Limit exceeded --> 429 Response
```

The rate limiter is particularly useful for authentication endpoints because login requests can otherwise be repeatedly attempted.

---

# Authentication

The API uses **JWT bearer authentication**.

The authentication flow is:

```text
Register
   |
   v
POST /auth/register
   |
   v
User Created
   |
   v
POST /auth/login
   |
   v
JWT Access Token
   |
   v
Authorization: Bearer <token>
   |
   v
Protected Endpoint
```

Protected routes require:

```text
Authorization: Bearer <access_token>
```

---

# User Roles

Registration supports two roles:

```text
user
admin
```

### User

A normal user can:

* Access authenticated user endpoints
* View users
* Create products
* View products
* Update products
* Upload files

### Admin

An administrator can perform the normal authenticated operations plus:

* Delete products

Role-based authorization is implemented through authentication dependencies.

---

# API Overview

All endpoints are rooted at `/`.

## General

| Method | Endpoint | Authentication | Purpose                 |
| ------ | -------- | -------------- | ----------------------- |
| `GET`  | `/`      | No             | Health/welcome response |

## Authentication

| Method | Endpoint         | Authentication | Purpose                     |
| ------ | ---------------- | -------------- | --------------------------- |
| `POST` | `/auth/register` | No             | Register a user             |
| `POST` | `/auth/login`    | No             | Authenticate and return JWT |

The login endpoint is rate-limited to **3 requests per minute**.

Login accepts form-encoded:

```text
username = user's email
password = user's password
```

---

## Users

| Method | Endpoint           | Authentication | Purpose                          |
| ------ | ------------------ | -------------- | -------------------------------- |
| `GET`  | `/users/me`        | Yes            | Get authenticated user's profile |
| `GET`  | `/users/`          | Yes            | List users                       |
| `GET`  | `/users/{user_id}` | Yes            | Get user by ID                   |

---

## Products

| Method   | Endpoint                 | Authentication | Purpose           |
| -------- | ------------------------ | -------------- | ----------------- |
| `POST`   | `/products/`             | Yes            | Create a product  |
| `GET`    | `/products/`             | Yes            | List products     |
| `GET`    | `/products/{product_id}` | Yes            | Get product by ID |
| `PUT`    | `/products/{product_id}` | Yes            | Update a product  |
| `DELETE` | `/products/{product_id}` | Admin          | Delete a product  |

Product creation accepts:

```json
{
  "name": "Laptop",
  "price": 75000,
  "description": "Development laptop"
}
```

The product is associated with the authenticated user.

---

## File Upload

| Method | Endpoint        | Authentication | Purpose                             |
| ------ | --------------- | -------------- | ----------------------------------- |
| `POST` | `/files/upload` | Yes            | Upload an authenticated user's file |

Uploaded files are stored in:

```text
uploads/
```

---

# Project Structure

```text
user-product-api/
│
├── app/
│   ├── auth/
│   │   ├── dependencies.py
│   │   └── jwt.py
│   │
│   ├── core/
│   │   └── limiter.py
│   │
│   ├── models/
│   │   ├── product.py
│   │   └── user.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── files.py
│   │   ├── products.py
│   │   └── users.py
│   │
│   ├── schemas/
│   │   ├── product.py
│   │   ├── settings.py
│   │   └── user.py
│   │
│   ├── database.py
│   └── main.py
│
├── tests/
│   ├── test_login.py
│   ├── test_main.py
│   └── test_register.py
│
├── uploads/
│
├── .dockerignore
├── .env
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# Application Architecture

```text
                       Client
                         |
                         v
                ┌─────────────────┐
                │ Logging         │
                │ Middleware      │
                │                 │
                │ Method          │
                │ Path            │
                │ Status Code     │
                │ Execution Time  │
                └────────┬────────┘
                         |
                         v
                ┌─────────────────┐
                │   Rate Limiter  │
                └────────┬────────┘
                         |
                         v
                ┌─────────────────┐
                │    FastAPI      │
                │     Router      │
                └────────┬────────┘
                         |
             ┌───────────┼───────────┐
             |           |           |
             v           v           v
           Auth        Users      Products
             |           |           |
             └───────────┼───────────┘
                         |
                         v
                JWT Authentication
                         |
                         v
                  SQLAlchemy ORM
                         |
                         v
                    PostgreSQL
```

---

# Configuration

Create `.env` in the project root:

```dotenv
db_password=your-database-password
SECRET_KEY=your-long-random-secret-key
ALGORITHM=HS256
```

Optional database override:

```powershell
$env:DATABASE_URL = "postgresql+psycopg2://postgres:your-password@localhost:5432/user_product_db"
```

Do not commit `.env` or production credentials to Git.

---

# Running Locally

Create the virtual environment:

```powershell
py -3.12 -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the API:

```powershell
python -m uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# Running with Docker Compose

Build and start the API and PostgreSQL:

```powershell
docker compose up --build
```

The API is available at:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Check containers:

```powershell
docker compose ps
```

View API logs:

```powershell
docker compose logs api
```

View database logs:

```powershell
docker compose logs db
```

Stop the services:

```powershell
docker compose down
```

PostgreSQL data is persisted in the `postgres_data` Docker volume.

---

# Testing

The project uses `pytest` and FastAPI's `TestClient`.

Install testing dependencies:

```powershell
python -m pip install pytest httpx
```

Run all tests:

```powershell
python -m pytest
```

Run with verbose output:

```powershell
python -m pytest -v -s
```

Current tests:

```text
tests/test_main.py
tests/test_register.py
tests/test_login.py
```

The tests verify:

* Application/OpenAPI availability
* User registration
* Successful login
* JWT access-token generation

---

# Security

The application includes several security-related mechanisms:

### JWT Authentication

Protected endpoints require a valid JWT bearer token.

### Password Hashing

User passwords are hashed before being stored.

### Role-Based Authorization

Administrative operations require the `admin` role.

### Rate Limiting

Login requests are limited to:

```text
3 requests/minute
```

### Request Logging

Middleware records:

```text
HTTP method
Request path
Response status
Execution time
```

### Environment Variables

Sensitive configuration such as:

```text
SECRET_KEY
db_password
DATABASE_URL
```

is provided through environment variables.

---

# Docker Architecture

```text
                     Docker Compose
                           |
              ┌────────────┴────────────┐
              |                         |
              v                         v
       ┌──────────────┐          ┌──────────────┐
       │   FastAPI    │          │ PostgreSQL   │
       │     API      │─────────>│      DB      │
       │              │  db:5432 │              │
       └──────────────┘          └───────┬──────┘
              |                          |
              |                          v
              |                    postgres_data
              |
              v
       Port 8000
              |
              v
          Browser
       /docs /redoc
```

---

# Docker Commands

Build and start:

```powershell
docker compose up --build
```

Run in background:

```powershell
docker compose up -d
```

Check containers:

```powershell
docker compose ps
```

View all logs:

```powershell
docker compose logs
```

Follow API logs:

```powershell
docker compose logs -f api
```

Stop:

```powershell
docker compose down
```

Remove containers and database volume:

```powershell
docker compose down -v
```

> `docker compose down -v` permanently removes the PostgreSQL Docker volume and its stored database data.

---

# Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

Swagger can be used to:

* Register users
* Login
* Authorize with JWT
* Test protected endpoints
* Create products
* Update products
* Delete products as an admin
* Upload files
* Inspect request and response schemas

---

# License

This project is intended for learning, development, and portfolio purposes.
