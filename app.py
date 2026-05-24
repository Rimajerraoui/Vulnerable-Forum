from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "1234"  # ⚠️ BEWUSSTE LÜCKE: schwacher Secret Key

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
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]  # ⚠️ BEWUSSTE LÜCKE: Klartext Passwort
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
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
        # ⚠️ BEWUSSTE LÜCKE: SQL Injection
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        user = c.execute(query).fetchone()
        conn.close()
        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/forum")
        return render_template("login.html", error="Falscher Benutzername oder Passwort!")
    return render_template("login.html")

@app.route("/forum", methods=["GET", "POST"])
def forum():
    if "user_id" not in session:
        return redirect("/login")
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]  # ⚠️ BEWUSSTE LÜCKE: Stored XSS
        c.execute("INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
                  (session["user_id"], title, content))
        conn.commit()
    posts = c.execute("SELECT * FROM posts").fetchall()
    conn.close()
    return render_template("forum.html", posts=posts, username=session["username"])

@app.route("/post/new", methods=["GET", "POST"])
def new_post():
    if "user_id" not in session:
        return redirect("/login")
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
                  (session["user_id"], title, content))
        conn.commit()
        conn.close()
        return redirect("/forum")
    return render_template("new_post.html")

if __name__ == "__main__":
    app.run(debug=True)