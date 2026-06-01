from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "1234"  #  BEWUSSTE LÜCKE: schwacher Secret Key , Angreifer kann es leicht faelschen

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

@app.route("/register", methods=["GET", "POST"])# broken authentication
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]  #  BEWUSSTE LÜCKE: Passwoerter sind in DB lesbar (broken audentication)
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"]) #SQL Injecton
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        # BEWUSSTE LÜCKE: SQL Injection , login ohne passwort moeglich
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        user = c.execute(query).fetchone()
        conn.close()
        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/forum")
        return render_template("login.html", error="Ihre Anmeldung war leider nicht erfolgreich. Bitte versuchen Sie es noch einmal und prüfen Sie die Benutzername und das Passwort!")
    return render_template("login.html")

@app.route("/forum", methods=["GET", "POST"]) #XSS
def forum():
    if "user_id" not in session:
        return redirect("/login")
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]  # BEWUSSTE LÜCKE: Stored XSS , ,wird das bei jedem ausgefuehrt der das Forum oeffnet.
        c.execute("INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
                  (session["user_id"], title, content))
        conn.commit()
    posts = c.execute("SELECT * FROM posts").fetchall()
    conn.close()
    return render_template("forum.html", posts=posts, username=session["username"])

@app.route("/post/new", methods=["GET", "POST"])
def neue_post():
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

@app.route("/usercheck") #Blind SQL Injection
def usercheck():
    username = request.args.get("username")
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    query= f"SELECT * FROM users WHERE username='{username}'"
    user = c.execute(query).fetchone()
    if  user:
        return "User gefunden"
    else:
        return "User nicht gefunden"

@app.route("/search")
def search():
    query = request.args.get("q", "")

    # Reflected XSS ist in search.html durch {{ query|safe }}
    return render_template("search.html", query=query)

@app.route("/post/<id>") #IDOR
def zeig_post(id):
    if "user_id" not in session:
        return redirect("/login")
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = ?",(id,))
    post = c.fetchone()
    conn.close()

    return f"Titel: {post[2]} - Inhalt: {post[3]}"


@app.route("/files/") #Path Traversal
def herunterladen():
    filename = request.args.get("name")  # kommt aus URL Parameter
    with open("uploads/" + filename, encoding="utf-8", errors="ignore") as f:  #BEWUSSTE LÜCKE: Path Traversal
        inhalt = f.read()
    return inhalt




if __name__ == "__main__":
    app.run(debug=True)