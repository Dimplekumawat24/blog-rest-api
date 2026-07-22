"""
Populates the database with a few sample users, posts, and comments
so the app has something to look at right after setup.

Run with:  python seed.py
"""
from app import create_app
from app.models import db, User, Post, Comment

app = create_app()

with app.app_context():
    if User.query.first():
        print("Database already has data — skipping seed. Delete blog.db to start fresh.")
    else:
        arjun = User(username="arjun_verma")
        arjun.set_password("password123")
        priya = User(username="priya_dev")
        priya.set_password("password123")
        db.session.add_all([arjun, priya])
        db.session.commit()

        post1 = Post(
            title="Designing clean REST routes for a blog API",
            content="A look at resource naming, status codes, and how to keep routes predictable as the API grows.",
            tags="flask,rest,design",
            author_id=arjun.id,
        )
        post2 = Post(
            title="Adding JWT authentication to a Flask API",
            content="Token issuing and protecting write endpoints without over-engineering the auth layer.",
            tags="flask,auth,jwt",
            author_id=priya.id,
        )
        db.session.add_all([post1, post2])
        db.session.commit()

        db.session.add(Comment(body="This matches the structure I ended up with too.", post_id=post1.id, author_id=priya.id))
        db.session.commit()

        print("Seeded 2 users, 2 posts, 1 comment.")
        print("Sample login -> username: arjun_verma  password: password123")
