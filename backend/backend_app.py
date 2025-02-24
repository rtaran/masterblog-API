from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Configure JWT authentication
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

# Correct Limiter initialization
limiter = Limiter(
    key_func=get_remote_address
)
limiter.init_app(app)  # Attach Limiter to Flask app

# Hardcoded list of blog posts
POSTS = [
    {
        "id": 1,
        "title": "Flask API",
        "content": "Learn how to build APIs with Flask.",
        "category": "Programming",
        "tags": ["Python", "Flask", "API"],
        "comments": [
            {"user": "Alice", "text": "Great post!"},
            {"user": "Bob", "text": "Thanks for the info!"}
        ]
    }
]

# User authentication (Login)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data["username"] == "admin" and data["password"] == "password":
        access_token = create_access_token(identity=data["username"])
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid credentials"}), 401

# GET all posts with sorting & pagination
@app.route('/api/posts', methods=['GET'])
@limiter.limit("10 per minute")  # Rate limiting applied
def get_posts():
    """Fetch all blog posts with optional sorting and pagination."""
    sort_by = request.args.get('sort', None)
    direction = request.args.get('direction', 'asc').lower()
    page = request.args.get('page', type=int, default=1)
    limit = request.args.get('limit', type=int, default=5)

    valid_sort_fields = {"title", "content"}
    valid_directions = {"asc", "desc"}

    if sort_by and sort_by not in valid_sort_fields:
        return jsonify({"error": "Invalid sort field. Use 'title' or 'content'."}), 400

    if direction not in valid_directions:
        return jsonify({"error": "Invalid direction. Use 'asc' or 'desc'."}), 400

    sorted_posts = sorted(POSTS, key=lambda x: x[sort_by].lower(), reverse=direction == "desc") if sort_by else POSTS

    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_posts = sorted_posts[start_index:end_index]

    return jsonify({
        "page": page,
        "limit": limit,
        "total_posts": len(POSTS),
        "total_pages": (len(POSTS) + limit - 1) // limit,
        "posts": paginated_posts
    }), 200

# Create a new post (Authenticated)
@app.route('/api/posts', methods=['POST'])
@jwt_required()
def add_post():
    """Add a new blog post with authentication."""
    data = request.json

    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Title and content are required"}), 400

    new_id = max(post["id"] for post in POSTS) + 1 if POSTS else 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"],
    }

    POSTS.append(new_post)
    return jsonify(new_post), 201  # 201 Created

# Delete a post
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """Delete a blog post by ID with error handling."""
    post_to_delete = next((post for post in POSTS if post["id"] == post_id), None)

    if not post_to_delete:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    POSTS.remove(post_to_delete)  # Modify list in place
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

# Update a post
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    """Update a blog post by ID, keeping old values if not provided."""
    data = request.json
    post_to_update = next((post for post in POSTS if post["id"] == post_id), None)

    if not post_to_update:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    post_to_update["title"] = data.get("title", post_to_update["title"])
    post_to_update["content"] = data.get("content", post_to_update["content"])

    return jsonify(post_to_update), 200  # 200 OK

# Search for posts
@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Search for blog posts by title or content."""
    title_query = request.args.get('title', '').strip().lower()
    content_query = request.args.get('content', '').strip().lower()

    if not title_query and not content_query:
        return jsonify({"error": "Please provide a search query"}), 400

    matching_posts = [
        post for post in POSTS
        if title_query in post["title"].lower() or content_query in post["content"].lower()
    ]

    return jsonify(matching_posts), 200  # Return matching posts

# API versioning
@app.route('/api/v1/posts', methods=['GET'])
def get_posts_v1():
    return jsonify(POSTS)

@app.route('/api/v2/posts', methods=['GET'])
def get_posts_v2():
    return jsonify({"message": "New version with better features!"})

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)