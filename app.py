from flask import Flask, render_template, request, session, redirect
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "1234"  # BEWUSSTE LÜCKE: schwacher Secret Key


def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT DEFAULT 'user'
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            content TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]  # BEWUSSTE LÜCKE: Passwort im Klartext

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # BEWUSSTE LÜCKE: SQL Injection
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        user = c.execute(query).fetchone()

        conn.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/forum")

        return "Falsche Daten!"

    return render_template("login.html")


@app.route("/forum", methods=["GET", "POST"])
def forum():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]  # BEWUSSTE LÜCKE: Stored XSS möglich

        c.execute(
            "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
            (session["user_id"], title, content)
        )
        conn.commit()

    posts = c.execute("SELECT * FROM posts").fetchall()
    conn.close()

    return render_template(
        "forum.html",
        username=session["username"],
        posts=posts
    )


@app.route("/post/new", methods=["GET", "POST"])
def new_post():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
            (session["user_id"], title, content)
        )
        conn.commit()
        conn.close()

        return redirect("/forum")

    return render_template("new_post.html")


@app.route("/post/<id>")
def show_post(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # BEWUSSTE LÜCKE: IDOR, Nutzer kann fremde Posts über ID ansehen
    c.execute("SELECT * FROM posts WHERE id = ?", (id,))
    post = c.fetchone()

    conn.close()

    if not post:
        return "Post nicht gefunden"

    return f"Titel: {post[2]}<br>Inhalt: {post[3]}"


@app.route("/search")
def search():
    query = request.args.get("q", "")

    # Reflected XSS ist in search.html durch {{ query|safe }}
    return render_template("search.html", query=query)


@app.route("/usercheck")
def usercheck():
    username = request.args.get("username", "")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # BEWUSSTE LÜCKE: Blind SQL Injection
    query = f"SELECT * FROM users WHERE username='{username}'"
    user = c.execute(query).fetchone()

    conn.close()

    if user:
        return "User gefunden"
    else:
        return "User nicht gefunden"


@app.route("/files")
def files():
    filename = request.args.get("name", "")

    # BEWUSSTE LÜCKE: Path Traversal
    with open("uploads/" + filename, encoding="utf-8", errors="ignore") as f:
        content = f.read()

    return content


if __name__ == "__main__":
    app.run(debug=True)