from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Hardcoded list of blog posts
POSTS = [
    {"id": 1, "title": "First Post", "content": "This is the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the second post."},
]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Fetch all blog posts with optional sorting and pagination."""
    sort_by = request.args.get('sort', None)
    direction = request.args.get('direction', 'asc').lower()
    page = request.args.get('page', 1, type=int)  # Default to page 1
    limit = request.args.get('limit', 5, type=int)  # Default to 5 posts per page

    valid_sort_fields = {"title", "content"}
    valid_directions = {"asc", "desc"}

    # Error handling: Check if provided sorting fields are valid
    if sort_by and sort_by not in valid_sort_fields:
        return jsonify({"error": "Invalid sort field. Use 'title' or 'content'."}), 400

    if direction not in valid_directions:
        return jsonify({"error": "Invalid direction. Use 'asc' or 'desc'."}), 400

    # If a valid sort field is provided, sort posts accordingly
    sorted_posts = POSTS
    if sort_by:
        reverse_order = direction == "desc"
        sorted_posts = sorted(POSTS, key=lambda x: x[sort_by].lower(), reverse=reverse_order)

    # Implement pagination
    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_posts = sorted_posts[start_index:end_index]

    return jsonify({
        "page": page,
        "limit": limit,
        "total_posts": len(POSTS),
        "total_pages": (len(POSTS) + limit - 1) // limit,  # Calculate total pages
        "posts": paginated_posts
    }), 200

@app.route('/api/posts', methods=['POST'])
def add_post():
    """Add a new blog post with error handling."""
    data = request.json

    # Validate input
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Title and content are required"}), 400

    # Generate a new unique ID
    new_id = max(post["id"] for post in POSTS) + 1 if POSTS else 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"],
    }

    POSTS.append(new_post)
    return jsonify(new_post), 201  # 201 Created

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a blog post by ID with error handling."""
    global POSTS
    post_to_delete = next((post for post in POSTS if post["id"] == post_id), None)

    if not post_to_delete:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    POSTS = [post for post in POSTS if post["id"] != post_id]
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a blog post by ID, keeping old values if not provided."""
    data = request.json
    post_to_update = next((post for post in POSTS if post["id"] == post_id), None)

    if not post_to_update:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    # Update fields only if they are provided in the request
    post_to_update["title"] = data.get("title", post_to_update["title"])
    post_to_update["content"] = data.get("content", post_to_update["content"])

    return jsonify(post_to_update), 200  # 200 OK

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Search for blog posts by title or content."""
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    # Filter posts based on search criteria
    matching_posts = [
        post for post in POSTS
        if title_query in post["title"].lower() or content_query in post["content"].lower()
    ]


    return jsonify(matching_posts), 200  # Return matching posts

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)