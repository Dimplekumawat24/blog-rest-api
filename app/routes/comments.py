from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import db, Post, Comment

comments_bp = Blueprint("comments", __name__, url_prefix="/api")


@comments_bp.get("/posts/<int:post_id>/comments")
def list_comments(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "post not found"}), 404
    return jsonify([c.to_dict() for c in post.comments]), 200


@comments_bp.post("/posts/<int:post_id>/comments")
@jwt_required()
def add_comment(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "post not found"}), 404

    data = request.get_json(silent=True) or {}
    body = (data.get("body") or "").strip()
    if not body:
        return jsonify({"error": "comment body is required"}), 400

    user_id = int(get_jwt_identity())
    comment = Comment(body=body, post_id=post_id, author_id=user_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201


@comments_bp.delete("/comments/<int:comment_id>")
@jwt_required()
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "comment not found"}), 404

    user_id = int(get_jwt_identity())
    if comment.author_id != user_id:
        return jsonify({"error": "you can only delete your own comments"}), 403

    db.session.delete(comment)
    db.session.commit()
    return "", 204
