# 🚀 Masterblog API

Masterblog API is a full-stack blog platform with a Flask-powered RESTful backend and a simple web-based frontend. It demonstrates modern Python backend design patterns, token-based user authentication, and essential CRUD operations via an API consumed by a dynamic frontend.

---

## 🗂️ Project Structure
masterblog+API/ ├── backend/ │ └── backend_app.py ├── frontend/ │ ├── static/ │ ├── templates/ │ └── frontend_app.py ├── .gitignore ├── LICENSE └── README.md

---

## ✨ Features

- REST API for managing blog posts (Create, Read, Delete)
- User authentication with JWT tokens
- Search posts by keyword
- Sorting and pagination of posts
- Rate limiting and CORS support
- Simple, clean frontend to interact with the API

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.12+
- [virtualenv](https://virtualenv.pypa.io/)

### Installation

1. **Clone the repository:**
    ```bash
    git clone git@github.com:rtaran/masterblog-API.git
    cd masterblog-API
    ```

2. **Create & activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚦 Running the Application

1. **Start the backend API:**
    ```bash
    python backend/backend_app.py
    ```
    - Default: http://localhost:5002

2. **Start the frontend application:**
    ```bash
    python frontend/frontend_app.py
    ```
    - Default: http://localhost:5001

---

## 🔌 API Endpoints Overview

- **Authentication**
  - `POST /api/login` — obtain JWT token

- **Posts**
  - `GET /api/posts` — list all posts, supports sorting & pagination
  - `POST /api/posts` — create new post (JWT required)
  - `DELETE /api/posts/<id>` — remove a post by ID (JWT required)
  - `GET /api/posts/search` — search for posts by keyword

**API query parameters:**  
- `sort` (title, content, author, date),  
- `direction` (asc, desc),  
- `page` (int),  
- `limit` (int),  
- `query` (str, for search endpoint)

---

## 🖥️ Frontend

Visit http://localhost:5001 after starting both servers to use the web UI.

---

## 🧪 Testing

To run all tests, ensure the virtual environment is activated, then:
bash pytest

---

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for details.