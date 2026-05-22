<<<<<<< HEAD
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/forum", methods=["GET", "POST"])
def forum():
    return render_template("forum.html")
=======
from flask import Flask, render_template, request, session, redirect
import sqlite3
app = Flask(__name__)
app.secret_key = "1234"


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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return "Registrierung erfolgreich!"
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # User Daten aus dem Formular holen
        username = request.form["username"]
        password = request.form["password"]
        
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        user = c.execute(query).fetchone() #fetchone gibt nur das erste Ergebnis aus
        
        if user:
            # Session speichern
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/forum")
        return "Falsche Daten!"
    return render_template("login.html")
@app.route("/forum")
def forum():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("forum.html", username=session["username"])

@app.route("/post/new" , methods=["GET","POST"])
def new_post():
    if "user_id" not in session:
        return redirect("/login")
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("INSERT INTO posts(user_id,title,content) VALUES(?,?,?)",(session["user_id"],title,content))

        conn.commit()
        conn.close()
        return redirect("/forum")
    return render_template("new_post.html")


>>>>>>> a24bcdf8261d4808174845a781b00413eaaf78c8

if __name__ == "__main__":
    app.run(debug=True)