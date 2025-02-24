from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Configure JWT authentication
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

# Configure request rate limiting
limiter = Limiter(key_func=get_remote_address)

# JSON File to store posts
POSTS_FILE = "posts.json"

# 🔹 Utility Functions for JSON File Handling
def load_posts():
    """Read posts from JSON file safely."""
    if not os.path.exists(POSTS_FILE):
        return []
    try:
        with open(POSTS_FILE, "r", encoding="utf-8") as file:
            data = file.read()
            return json.loads(data) if data.strip() else []
    except (json.JSONDecodeError, IOError):
        return []

def save_posts(posts):
    """Safely write posts to JSON file without corruption."""
    temp_file = POSTS_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4)
    os.replace(temp_file, POSTS_FILE)  # Atomically replace old file

# 🔹 User Authentication (Login)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data["username"] == "admin" and data["password"] == "password":
        access_token = create_access_token(identity=data["username"])
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid credentials"}), 401

# 🔹 GET `/api/posts` - Retrieve All Posts with Sorting & Pagination
@app.route('/api/posts', methods=['GET'])
@limiter.limit("10 per minute")
def get_posts():
    """Fetch all blog posts with optional sorting and pagination."""
    posts = load_posts()
    sort_by = request.args.get('sort', None)
    direction = request.args.get('direction', 'asc').lower()
    page = request.args.get('page', type=int, default=1)
    limit = request.args.get('limit', type=int, default=5)

    valid_sort_fields = {"title", "content", "author", "date"}
    valid_directions = {"asc", "desc"}

    if sort_by and sort_by not in valid_sort_fields:
        return jsonify({"error": "Invalid sort field."}), 400

    if direction not in valid_directions:
        return jsonify({"error": "Invalid sort direction."}), 400

    if sort_by == "date":
        sorted_posts = sorted(posts, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=direction == "desc")
    else:
        sorted_posts = sorted(posts, key=lambda x: x[sort_by].lower(), reverse=direction == "desc") if sort_by else posts

    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_posts = sorted_posts[start_index:end_index]

    return jsonify({
        "page": page,
        "limit": limit,
        "total_posts": len(posts),
        "total_pages": (len(posts) + limit - 1) // limit,
        "posts": paginated_posts
    }), 200

# 🔹 POST `/api/posts` - Create a New Post
@app.route('/api/posts', methods=['POST'])
@jwt_required()
def add_post():
    """Add a new blog post and save to JSON file."""
    posts = load_posts()
    data = request.json

    if not data or "title" not in data or "content" not in data or "author" not in data:
        return jsonify({"error": "Title, content, and author are required"}), 400

    date_str = data.get("date", datetime.today().strftime("%Y-%m-%d"))
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD'"}), 400

    new_id = max((post["id"] for post in posts), default=0) + 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"],
        "author": data["author"],
        "date": date_str
    }

    posts.append(new_post)
    save_posts(posts)
    return jsonify(new_post), 201

# 🔹 DELETE `/api/posts/<id>` - Remove a Post
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """Delete a blog post from JSON file."""
    posts = load_posts()
    post_to_delete = next((post for post in posts if post["id"] == post_id), None)

    if not post_to_delete:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    posts.remove(post_to_delete)
    save_posts(posts)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

# 🔹 Search for Posts
@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Search for blog posts by title, content, author, or date."""
    query = request.args.get('query', '').strip().lower()
    posts = load_posts()
    if not query:
        return jsonify([]), 200

    matching_posts = [post for post in posts if query in post["title"].lower() or
                      query in post["content"].lower() or query in post["author"].lower() or query in post["date"]]

    return jsonify(matching_posts), 200

# 🔹 Run the App
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)