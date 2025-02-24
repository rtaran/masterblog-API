import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]
@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)

@app.route('/api/posts', methods=['POST'])
def add_posts():
    data = request.json
    # Validate input
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Title and Content are required"}), 400
    # Generate a new unique ID
    new_id = max(post["id"] for post in POSTS) + 1 if POSTS else 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"],
    }

    POSTS.append(new_post)
    return jsonify(new_post), 201

@app.route('/api/posts/<id>', method=['POST'])
def del_posts():
    global POSTS
    posts_to_del = next((post for post in POSTS if post['id'] == id), None)

    if not posts_to_del:
        return  jsonify({"error": f"Post with id {id} not found"}), 404

    POSTS = [post for post in POSTS if post['id'] != 'id']
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
