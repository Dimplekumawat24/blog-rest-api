# Blog REST API

A working Flask REST API for blog management — posts, comments, and JWT
authentication — with a small frontend that talks to the real API (no mock
data, no fake responses). Everything in this zip actually runs.

## What's included

- **Backend**: Flask + Flask-SQLAlchemy + Flask-JWT-Extended
  - `POST /api/auth/register` — create an account
  - `POST /api/auth/login` — log in, receive a JWT
  - `GET /api/posts` — list all posts
  - `GET /api/posts/<id>` — a single post with its comments
  - `POST /api/posts` — create a post (login required)
  - `PUT /api/posts/<id>` — edit your own post (login required)
  - `DELETE /api/posts/<id>` — delete your own post (login required)
  - `GET /api/posts/<id>/comments` — list comments on a post
  - `POST /api/posts/<id>/comments` — add a comment (login required)
  - `DELETE /api/comments/<id>` — delete your own comment (login required)
- **Database**: SQLAlchemy models for `User`, `Post`, `Comment`. Uses SQLite
  out of the box (zero setup) — switch to MySQL by setting one environment
  variable (see below).
- **Frontend**: a single static page (`app/static/index.html`) served by
  Flask itself, styled as a small blog reader. It calls the real endpoints
  above with `fetch()` — logging in, writing posts, and commenting all hit
  the live API.

## Project structure

```
blog-rest-api/
├── app/
│   ├── __init__.py       # Flask app factory
│   ├── config.py         # database & JWT config
│   ├── models.py         # User, Post, Comment (SQLAlchemy)
│   ├── routes/
│   │   ├── auth.py       # register / login
│   │   ├── posts.py      # post CRUD
│   │   └── comments.py   # comment CRUD
│   └── static/
│       └── index.html    # frontend (served at /)
├── run.py                # starts the dev server
├── seed.py                # optional: adds sample data
├── requirements.txt
└── README.md
```

## 1. Prerequisites

- Python 3.9 or newer
- `pip` (comes with Python)

Check your version:

```bash
python3 --version
```

## 2. Unzip and enter the project

```bash
unzip blog-rest-api.zip
cd blog-rest-api
```

## 3. Create a virtual environment (recommended)

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

You'll know it worked when your terminal prompt starts with `(venv)`.

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Run the app

```bash
python run.py
```

You should see output ending with something like:

```
 * Running on http://127.0.0.1:5000
```

Open **http://localhost:5000** in your browser. A SQLite file `blog.db` is
created automatically in the project folder the first time you run it — no
database setup needed.

## 6. (Optional) Load sample data

In a second terminal (with the virtual environment activated):

```bash
python seed.py
```

This adds two sample users and two sample posts so the feed isn't empty.
Sample login:

- **username**: `arjun_verma`
- **password**: `password123`

Or just click "Register" in the app and create your own account — that
works too.

## 7. Using the app

- **Log in / Register**: top-right corner. Registering hits
  `POST /api/auth/register`, logging in hits `POST /api/auth/login`, and
  the JWT you get back is stored in the browser and sent as a
  `Authorization: Bearer <token>` header on every write request.
- **Write a post**: "Write a post" button (requires login).
- **Comment**: open any post and comment at the bottom (requires login).
- **Delete**: you can only delete posts and comments you authored — the
  API checks this server-side (returns `403` otherwise), not just in the
  UI.
- The dark strip under the nav bar shows whether the API is reachable and
  your current auth status. The sidebar lists every endpoint the frontend
  uses.

## 8. Testing the API directly (optional)

You don't need the frontend to use the API — it's a normal REST API and
works fine with `curl` or Postman:

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user", "password": "test1234"}'

# Log in (copy the access_token from the response)
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user", "password": "test1234"}'

# Create a post (replace <TOKEN> with the access_token above)
curl -X POST http://localhost:5000/api/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"title": "Hello", "content": "My first post", "tags": ["intro"]}'

# List posts (no auth needed)
curl http://localhost:5000/api/posts
```

## 9. Switching from SQLite to MySQL

By default the app uses a local SQLite file so it runs with no extra setup.
To point it at MySQL instead:

1. Create a database in MySQL:
   ```sql
   CREATE DATABASE blog_api;
   ```
2. Set the `DATABASE_URL` environment variable before running the app:

   **macOS / Linux**
   ```bash
   export DATABASE_URL="mysql+pymysql://<username>:<password>@localhost:3306/blog_api"
   python run.py
   ```

   **Windows (PowerShell)**
   ```powershell
   $env:DATABASE_URL="mysql+pymysql://<username>:<password>@localhost:3306/blog_api"
   python run.py
   ```

`PyMySQL` is already in `requirements.txt`, so no extra driver install is
needed. The app creates all tables automatically on startup either way.

## 10. Common issues

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Make sure your virtual environment is activated, then re-run `pip install -r requirements.txt`. |
| Port 5000 already in use | Edit `run.py` and change `port=5000` to another port, e.g. `port=5001`. |
| API strip says "unreachable" | The frontend and backend are served from the same Flask process — make sure `python run.py` is still running and you're using the URL it printed. |
| Changes to the database don't reset | Delete `blog.db` in the project folder and restart the app to start fresh (then optionally re-run `seed.py`). |

## Notes on scope

This is a portfolio-ready working demo, not a production deployment:
password hashing, JWT auth, and ownership checks (you can only edit/delete
your own content) are all real and enforced server-side. Things you'd add
before deploying publicly: HTTPS, rate limiting, refresh tokens, pagination
on the posts list, and moving `JWT_SECRET_KEY` out of source code into a
proper secrets manager.
