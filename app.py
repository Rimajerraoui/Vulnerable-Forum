from flask import Flask

app = Flask(__name__)
import sqlite3

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
    
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def start():
    return "Flask funktioniert!"

if __name__ == "__main__":
    app.run(debug=True)