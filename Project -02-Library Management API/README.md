# 📚 Library Management API

A RESTful Library Management System built with **FastAPI**, **MySQL**, and **SQLAlchemy**. This project provides APIs to manage books, users, and book borrowing operations.

---

## 🚀 Features

### 📖 Book Management
- Add a new book
- View all books
- View a single book
- Update book details
- Delete a book

### 👤 User Management
- Register a new user
- View all users
- View a single user
- Update user information
- Delete a user

### 📚 Borrow Management
- Borrow a book
- Return a book
- View borrow history
- Prevent borrowing the same book twice
- Prevent borrowing unavailable books
- Automatically update available book copies

---

## 🛠 Technologies Used

- Python 3
- FastAPI
- SQLAlchemy ORM
- MySQL
- PyMySQL
- Pydantic
- Uvicorn
- python-dotenv

---

## 📂 Project Structure

```
Library-Management-API/
│
├── routers/
│   ├── book.py
│   ├── user.py
│   └── borrow.py
│
├── pydantic_data/
│   ├── __init__.py
│   └── data_validation.py
│
├── database.py
├── models.py
├── main.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Library-Management-API.git

cd Library-Management-API
```

---

### 2. Create Virtual Environment

```bash
python -m venv myenv
```

Activate it

Windows

```bash
myenv\Scripts\activate
```

Linux / macOS

```bash
source myenv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a file named

```
.env
```

Add

```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/library_db
```

Replace

```
YOUR_PASSWORD
```

with your MySQL password.

---

### 5. Create Database

Open MySQL Workbench

Run

```sql
CREATE DATABASE library_db;
```

---

### 6. Create Tables

```bash
python create_table.py
```

---

### 7. Run the API

```bash
uvicorn main:app --reload
```

---

## 📌 API Documentation

After starting the server, open

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## 📋 API Endpoints

### 📚 Books

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /books | Get all books |
| GET | /books/{id} | Get single book |
| POST | /books | Add book |
| PUT | /books/{id} | Update book |
| DELETE | /books/{id} | Delete book |

---

### 👤 Users

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /user | Get all users |
| GET | /user/{id} | Get single user |
| POST | /user | Create user |
| PUT | /user/{id} | Update user |
| DELETE | /user/{id} | Delete user |

---

### 📖 Borrow

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /borrow | Borrow a book |
| POST | /borrow/return | Return a book |
| GET | /borrow | View borrow history |

---


## 🎯 Future Improvements

- JWT Authentication
- User Login
- Admin Dashboard
- Book Categories
- Search & Filter
- Pagination
- Alembic Database Migrations
- Docker Support
- Unit Testing
- CI/CD Pipeline

---

## 👨‍💻 Author

**Muhammad Zaid**

Software Engineering Student

Learning Backend Development with FastAPI, SQLAlchemy, and MySQL.

---

## ⭐ If you found this project useful

Please consider giving it a ⭐ on GitHub.