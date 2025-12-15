"""Flask API for managing blog posts.

This module provides a RESTful API for creating, reading, updating,
deleting, and searching blog posts.
"""

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
    """Get all posts with optional sorting.

    Query Parameters:
        sort (str): Field to sort by ('title' or 'content')
        direction (str): Sort direction ('asc' or 'desc'), default 'asc'

    Returns:
        tuple: JSON response with list of posts and status code 200
    """
    sort_tag = request.args.get('sort')
    direction_tag = request.args.get('direction', 'asc')

    posts = POSTS.copy()

    if sort_tag == 'title':
        def get_title(post):
            return post['title'].lower()

        if direction_tag.lower() == 'desc':
            reverse = True
        else:
            reverse = False

        posts = sorted(posts, key=get_title, reverse=reverse)

    elif sort_tag == 'content':
        def get_content(post):
            return post['content'].lower()

        if direction_tag.lower() == 'desc':
            reverse = True
        else:
            reverse = False

        posts = sorted(posts, key=get_content, reverse=reverse)

    return jsonify(posts), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Create a new post.

    Request Body:
        title (str): Post title (required)
        content (str): Post content (required)

    Returns:
        tuple: JSON response with created post and status code 201,
                or error message with status code 400
    """
    data = request.get_json()

    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({"error": "Please fill out required fields"}), 400

    new_post = {
        'id': len(POSTS) + 1,
        'title': title,
        'content': content
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by ID.

    Args:
        post_id (int): The ID of the post to delete

    Returns:
        tuple: JSON response with success message and status code 200,
                or error message with status code 404
    """
    for post in POSTS:

        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify({
                "success": f"Post with id ({post_id}) has been deleted successfully."
            }), 200

    return jsonify({
        "error": f"Post with id ({post_id}) do not exist."
    }), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a post by ID.

    Args:
        post_id (int): The ID of the post to update

    Request Body:
        title (str): New post title (optional)
        content (str): New post content (optional)

    Returns:
        tuple: JSON response with success message and status code 200,
                or error message with status code 400 or 404
    """
    data = request.get_json()

    new_title = data.get('title')
    new_content = data.get('content')

    for post in POSTS:

        if post['id'] == post_id:
            is_new_title = False
            if not new_title and not new_content:
                return jsonify({
                    "error": "Bad request: Nothing was changed"
                }), 400

            if new_title:
                is_new_title = True
                post['title'] = new_title

            if new_content:
                post['content'] = new_content
                if is_new_title:
                    return jsonify({
                        "message": f"title and content of post ({post_id}) was updated."
                    })
                return jsonify({
                    "message": f"content of post ({post_id}) was updated."
                })
            return jsonify({
                "message": f"title of post ({post_id}) was updated."
            })
    return jsonify({
        "error": f"Post with id ({post_id}) do not exist."
    }), 404


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    """Search posts by title or content.

    Query Parameters:
        title (str): Search term for title (optional)
        content (str): Search term for content (optional)

    Returns:
        tuple: JSON response with list of matching posts and status code 200,
                or error message with status code 400
    """
    title = request.args.get('title')
    content = request.args.get('content')

    if not title and not content:
        return jsonify({
            'error': 'Please provide title or content query'
        }), 400

    search_lst = []

    for post in POSTS:

        if title and title.lower() in post['title'].lower():
            search_lst.append(post)

        if content and content.lower() in post['content'].lower():
            if post not in search_lst:
                search_lst.append(post)

    return jsonify(search_lst), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)