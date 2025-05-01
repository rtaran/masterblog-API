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

## 🔐 Authentication

### Obtaining a JWT Token

To perform operations that require authentication (creating or deleting posts), you need to obtain a JWT token:

1. **Make a POST request to `/api/login` with the following credentials:**
   ```json
   {
     "username": "admin",
     "password": "password"
   }
   ```

2. **Example using curl:**
   ```bash
   curl -X POST http://localhost:5002/api/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "password"}'
   ```

3. **The response will contain your access token:**
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
   }
   ```

### Using the JWT Token

Include the token in the Authorization header for protected endpoints:

1. **Example of creating a new post with authentication:**
   ```bash
   curl -X POST http://localhost:5002/api/posts \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -d '{"title": "New Post", "content": "Post content", "author": "Your Name"}'
   ```

2. **Example of deleting a post with authentication:**
   ```bash
   curl -X DELETE http://localhost:5002/api/posts/1 \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

Replace `YOUR_ACCESS_TOKEN` with the actual token you received from the login endpoint.

---

## 🖥️ Frontend

Visit http://localhost:5001 after starting both servers to use the web UI.

> **Note:** The current frontend implementation does not include authentication functionality. To add or delete posts, you'll need to use API tools like curl or Postman with the JWT token as described in the Authentication section above. The web UI can still be used to view and search posts.

---

## 🧪 Testing

To run all tests, ensure the virtual environment is activated, then:
bash pytest

---

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for details.
