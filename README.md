# CloudShield

CloudShield is a Zero-Trust-inspired secure access gateway built with
FastAPI, PostgreSQL, Redis, Docker and JWT authentication.

The system authenticates users, evaluates access policies, applies
rate limits, records security audit logs, and securely forwards
authorized requests to internal services.

---

## Architecture

    Client
    |
    v
    CloudShield Gateway :8000
    |
    +--> JWT Authentication
    |
    +--> Redis Rate Limiting
    |
    +--> Policy Engine
    |
    +--> Audit Logging
    |       |
    |       v
    |   PostgreSQL
    |
    v
    Reverse Proxy
    |
    v
    Internal Backend :9000


Supporting Services:

Redis       -> Rate limiting
PostgreSQL  -> Users, policies and audit logs
Backend     -> Internal service
Docker      -> Containerization
Docker Compose -> Service orchestration

---

## Features

- JWT-based authentication
- Role-based access control
- Policy-based authorization
- Redis-backed rate limiting
- Reverse proxy / gateway
- PostgreSQL persistence
- Security audit logging
- Admin-only audit log access
- Security response headers
- Dockerized services
- Automated tests

---

## Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- HTTPX

### Security

- JWT
- bcrypt
- Role-based access control
- Policy-based authorization
- Rate limiting
- Audit logging

### Infrastructure

- Docker
- Docker Compose
- PostgreSQL
- Redis

### Testing

- pytest
- FastAPI TestClient

---

## Request Flow

A request to a protected internal resource follows this flow:

1. Client sends a request.
2. JWT authentication verifies the user's identity.
3. Redis checks the user's request rate.
4. Policy engine evaluates the user's role, resource and action.
5. The request is allowed or denied.
6. The decision is recorded in the audit log.
7. Authorized requests are forwarded to the internal service.
8. The internal service returns the response through the gateway.

---

## Example

Request:

GET /gateway/internal/data

Authentication:
JWT Bearer Token

Authorization:

Role: user
Resource: /internal/data
Action: GET

If the policy allows the request:

    ALLOW
    |
    v
    Reverse Proxy
    |
    v
    Internal Service

If the policy denies the request:

    DENY
    |
    v
    HTTP 403

The decision is recorded in PostgreSQL.

---

## Running Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd cloudshield