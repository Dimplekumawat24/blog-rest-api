from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import db, Post, User

posts_bp = Blueprint("posts", __name__, url_prefix="/api/posts")


@posts_bp.get("")
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts]), 200


@posts_bp.get("/<int:post_id>")
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "post not found"}), 404
    return jsonify(post.to_dict(include_comments=True)), 200


@posts_bp.post("")
@jwt_required()
def create_post():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()
    tags = data.get("tags") or []

    if not title or not content:
        return jsonify({"error": "title and content are required"}), 400

    if isinstance(tags, list):
        tags_str = ",".join(str(t).strip() for t in tags if str(t).strip())
    else:
        tags_str = str(tags)

    user_id = int(get_jwt_identity())
    post = Post(title=title, content=content, tags=tags_str, author_id=user_id)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201


@posts_bp.put("/<int:post_id>")
@jwt_required()
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "post not found"}), 404

    user_id = int(get_jwt_identity())
    if post.author_id != user_id:
        return jsonify({"error": "you can only edit your own posts"}), 403

    data = request.get_json(silent=True) or {}
    if "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"error": "title cannot be empty"}), 400
        post.title = title
    if "content" in data:
        content = (data.get("content") or "").strip()
        if not content:
            return jsonify({"error": "content cannot be empty"}), 400
        post.content = content
    if "tags" in data:
        tags = data.get("tags") or []
        post.tags = ",".join(str(t).strip() for t in tags if str(t).strip()) if isinstance(tags, list) else str(tags)

    db.session.commit()
    return jsonify(post.to_dict()), 200


@posts_bp.delete("/<int:post_id>")
@jwt_required()
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "post not found"}), 404

    user_id = int(get_jwt_identity())
    if post.author_id != user_id:
        return jsonify({"error": "you can only delete your own posts"}), 403

    db.session.delete(post)
    db.session.commit()
    return "", 204
