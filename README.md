# Org Management Assignment

A minimal organization management system built with FastAPI, providing endpoints for organization creation, admin login, and organization retrieval.

## Getting Started

### Prerequisites

Make sure you have Docker and Docker Compose installed.

### Run the Project

```bash
docker-compose up --build
```

This will start the FastAPI server on `http://localhost:8000`.

---

## 🧪 API Endpoints

### 1. Create Organization

```bash
curl --location 'http://localhost:8000/api/org/create' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "admin@company.com",
    "password": "securepassword",
    "organization_name": "My Company"
}'
```

---

### 2. Admin Login

```bash
curl --location 'http://localhost:8000/api/admin/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "admin@company.com",
    "password": "securepassword"
}'
```

This returns a JWT token to be used in the `Authorization` header for protected routes.

---

### 3. Get Organization Details

```bash
curl --location 'http://localhost:8000/api/org/get' \
--header 'Authorization: Bearer <your_jwt_token>' \
--header 'Content-Type: application/json' \
--data '{
    "organization_name": "My Company2"
}'
```

---