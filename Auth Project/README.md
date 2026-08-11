# FastAPI Authentication System

A production-oriented authentication backend built with **FastAPI**, **MySQL**, **SQLAlchemy**, and **JWT** authentication.

This project implements a complete authentication workflow covering user registration, login, access and refresh tokens, token revocation, logout, password recovery, password reset, role-based authorization, and frontend integration.

> **Project status:** Core authentication system completed.  
> **Scope:** Learning and portfolio project; additional hardening is required before production deployment.

---

## Overview

The goal of this project is to demonstrate how to design and structure a secure, maintainable authentication service using modern Python backend practices.

### Core capabilities

- User registration and validation
- Secure password hashing and verification
- JWT access-token authentication
- JWT refresh-token workflow
- Refresh-token revocation on logout
- Protected API routes
- Role-based authorization
- Admin-only endpoints
- Forgot-password workflow
- Secure password-reset tokens
- MySQL database integration
- SQLAlchemy ORM
- Pydantic request/response validation
- CORS configuration
- Frontend-to-API integration
- Environment-based configuration

---

## Features

### User Registration

Users can register with:

- Username
- Email
- Password

The backend validates uniqueness for usernames and email addresses and hashes passwords before persistence.

**Plain-text passwords are never stored in the database.**

### Authentication

After a successful login, the API issues:

- **Access token** — short-lived token for protected API requests
- **Refresh token** — longer-lived token used to obtain a new access token

Example response:

```json
{
  "access_token": "JWT_ACCESS_TOKEN",
  "refresh_token": "JWT_REFRESH_TOKEN",
  "token_type": "bearer"
}
```

### JWT Access Tokens

Access tokens authenticate requests to protected endpoints.

Typical payload:

```json
{
  "sub": "user_id",
  "exp": "expiration_time",
  "type": "access"
}
```

Default lifetime:

**15 minutes**

### Refresh Tokens

Refresh tokens allow clients to obtain a new access token without requiring the user to log in again.

Typical payload:

```json
{
  "sub": "user_id",
  "exp": "expiration_time",
  "type": "refresh"
}
```

Default lifetime:

**7 days**

### Logout and Token Revocation

The application maintains refresh-token revocation.

On logout:

1. The refresh token is validated.
2. The token is recorded in the revoked-token table.
3. The revoked token can no longer be used to issue a new access token.

This prevents a previously issued refresh token from being reused after logout.

### Protected Routes

Protected endpoints use FastAPI dependency injection through:

```python
get_current_user()
```

The dependency:

1. Extracts the Bearer token.
2. Decodes and validates the JWT.
3. Retrieves the user ID.
4. Loads the user from the database.
5. Returns the authenticated user.

### Role-Based Authorization

The project supports role-based authorization through:

```python
require_admin()
```

Endpoints protected by this dependency can be accessed only by users whose role is:

```text
admin
```

Unauthorized users receive:

```text
403 Forbidden
```

### Forgot Password and Password Reset

The password-recovery workflow uses secure, hashed reset tokens.

#### Request reset

1. User submits an email address.
2. Backend generates a secure random reset token.
3. The token is hashed.
4. The hash and expiration information are stored.

#### Reset password

1. Reset token is validated.
2. Expiration is checked.
3. Associated user is validated.
4. New password is hashed.
5. User password is updated.
6. Reset token is invalidated.

Invalidating the token prevents reuse.

---

## Architecture

```text
Auth Project/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── security.py
│
├── routers/
│   └── auth.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── images/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### Backend modules

| Module | Responsibility |
|---|---|
| `main.py` | FastAPI application entry point, router registration, middleware, and CORS |
| `database.py` | SQLAlchemy engine, session, declarative base, and database dependency |
| `models.py` | SQLAlchemy database models such as `User` and `RevokedToken` |
| `schemas.py` | Pydantic request and response validation |
| `security.py` | Password hashing, JWT handling, reset-token generation, authentication, and authorization |
| `routers/auth.py` | Authentication API endpoints |
| `frontend/` | Demonstration frontend for interacting with the authentication API |

---

## Authentication Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|:---:|
| `POST` | `/auth/signup` | Register a new user | No |
| `POST` | `/auth/login` | Authenticate a user | No |
| `POST` | `/auth/refresh` | Generate a new access token | No |
| `POST` | `/auth/logout` | Revoke a refresh token | No |
| `POST` | `/auth/forgot-password` | Request password reset | No |
| `POST` | `/auth/reset-password` | Reset the account password | No |

---

## Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Backend programming language |
| **FastAPI** | REST API framework |
| **SQLAlchemy** | ORM and database abstraction |
| **MySQL** | Relational database |
| **PyMySQL** | MySQL database driver |
| **Pydantic** | Request and response validation |
| **PyJWT** | JWT creation and validation |
| **pwdlib** | Password hashing and verification |
| **Uvicorn** | ASGI application server |
| **HTML** | Frontend structure |
| **CSS** | Frontend styling |
| **JavaScript** | Frontend API communication |

---

## Security Design

Security is treated as a first-class concern throughout the authentication workflow.

### Password hashing

Passwords are hashed with `pwdlib` before storage:

```python
password_hash.hash(password)
```

During authentication, the submitted password is verified against the stored hash:

```python
password_hash.verify(
    plain_password,
    hashed_password
)
```

### JWT signing

The application uses JWTs for stateless authentication and signs tokens using:

```text
HS256
```

### Refresh-token validation

Refresh tokens are checked for:

- Valid signature
- Expiration
- Correct token type
- Existing user
- Revocation status

### Reset-token protection

Password-reset tokens follow this pattern:

```text
Raw Reset Token
       │
       ▼
   SHA-256 Hash
       │
       ▼
    Database
```

The raw reset token is not stored directly in the database.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/fastapi-authentication-system.git
cd fastapi-authentication-system
```

### 2. Create a virtual environment

#### Windows

```powershell
python -m venv myenv
myenv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Database Configuration

Create a MySQL database:

```sql
CREATE DATABASE auth_db;
```

Do **not** hard-code database credentials or secrets in source code.

Create a local `.env` file:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/auth_db
SECRET_KEY=YOUR_LONG_RANDOM_SECRET_KEY
ALGORITHM=HS256
```

### Environment variables

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | SQLAlchemy connection string |
| `SECRET_KEY` | Secret used to sign JWTs |
| `ALGORITHM` | JWT signing algorithm |

For GitHub, commit only a safe template such as `.env.example`:

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost/auth_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
```

**Never commit `.env` or real credentials.**

---

## Running the Application

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

Swagger UI can be used to manually test authentication endpoints during development.

---

## Authentication Flow

```text
                    ┌───────────────┐
                    │    Signup     │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ User Database │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │     Login     │
                    └───────┬───────┘
                            │
                            ▼
               ┌────────────────────────┐
               │ Access + Refresh Token │
               └───────────┬────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
      Access Token                Refresh Token
             │                           │
             ▼                           ▼
      Protected API                /auth/refresh
                                         │
                                         ▼
                                  New Access Token
```

### Logout flow

```text
Client
  │
  ▼
/auth/logout
  │
  ▼
Validate Refresh Token
  │
  ▼
Store Token in RevokedToken
  │
  ▼
Refresh Token Rejected
```

---

## Password Reset Flow

```text
User
 │
 │ Forgot Password
 ▼
/auth/forgot-password
 │
 ▼
Generate Secure Token
 │
 ▼
Hash Token
 │
 ▼
Store Hash + Expiration
 │
 ▼
User Submits Reset Token
 │
 ▼
Validate Token
 │
 ▼
Hash New Password
 │
 ▼
Update User Password
 │
 ▼
Invalidate Reset Token
```

---

## Frontend

A lightweight frontend is included to demonstrate communication between the browser and the FastAPI backend.

It provides:

- Registration form
- Login form
- Forgot-password form
- Password-reset workflow
- Authentication feedback
- Registration feedback
- API communication using JavaScript `fetch()`

Frontend structure:

```text
frontend/
├── index.html
├── style.css
├── script.js
└── images/
```

---

## Testing

The API can be tested with:

- FastAPI Swagger UI
- Frontend application
- Postman
- Thunder Client

### Recommended test sequence

1. Register a user.
2. Log in.
3. Access a protected endpoint.
4. Refresh the access token.
5. Log out.
6. Attempt to reuse the revoked refresh token.
7. Request a password reset.
8. Reset the password.
9. Log in using the new password.

---

## Project Status

### Completed

- [x] User registration
- [x] Password hashing
- [x] User login
- [x] JWT access tokens
- [x] JWT refresh tokens
- [x] Refresh-token validation
- [x] Logout
- [x] Refresh-token revocation
- [x] Protected routes
- [x] Admin authorization
- [x] Forgot-password workflow
- [x] Password reset
- [x] Reset-token hashing
- [x] MySQL integration
- [x] SQLAlchemy ORM
- [x] Frontend integration
- [x] CORS configuration
- [x] Environment variables
- [x] GitHub-ready configuration

---

## Roadmap

Potential improvements for future versions:

- [ ] Email delivery for password-reset links
- [ ] Email verification
- [ ] Account activation
- [ ] Refresh-token rotation
- [ ] HTTP-only secure cookies
- [ ] Login-attempt limiting
- [ ] Rate limiting
- [ ] Account lockout
- [ ] Password-strength validation
- [ ] Change-password endpoint
- [ ] User profile endpoint
- [ ] Admin user-management endpoints
- [ ] Automated tests with Pytest
- [ ] Database migrations with Alembic
- [ ] Docker support
- [ ] Production deployment
- [ ] CI/CD pipeline
- [ ] Structured application logging

---

## Production Security Checklist

Before deploying this project to production:

- Generate a strong, unpredictable `SECRET_KEY`.
- Never commit `.env` files.
- Never commit database credentials.
- Use HTTPS.
- Configure explicit CORS origins.
- Use secure, HTTP-only cookies where appropriate for browser authentication.
- Add rate limiting to authentication endpoints.
- Deliver password-reset links through a trusted email service.
- Do not expose raw password-reset tokens through API responses or logs.
- Add automated security and integration tests.
- Review token lifetime and revocation strategy for the deployment environment.

> **Important:** This repository is currently a learning and portfolio project. It should undergo additional security hardening, testing, monitoring, and deployment review before being used in a production environment.

---

## Repository Hygiene

Before pushing to GitHub, make sure sensitive and generated files are excluded:

```gitignore
.env
myenv/
__pycache__/
*.pyc
```

Your repository should contain `.env.example`, not your real `.env`.

---

## Author

**M-ZAID**

Software Engineering Student focused on backend development, Python, FastAPI, databases, and software engineering.

---

## License

This project is available for **educational and portfolio purposes**.

---

## Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
