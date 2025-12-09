from flask import Flask, request, render_template_string
import sqlite3
import os  # 👈 أضيفي هذا السطر

app = Flask(__name__)

# ✅ FIXED: Secure login route
@app.route("/", methods=["GET", "POST"])
def home():
    msg = ""
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        
        conn = sqlite3.connect("app.db")
        cur = conn.cursor()
        
        # ✅ FIXED: Parameterized query (prevents SQL injection)
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        
        result = cur.fetchone()

        if result:
            msg = "Login successful!"
        else:
            msg = "Invalid credentials."

    return render_template_string("""
        <h2>Login</h2>
        <form method="POST">
            <input name="user" placeholder="User"><br>
            <input name="pwd" placeholder="Password"><br>
            <button>Login</button>
        </form>
        <p>{{msg}}</p>
    """, msg=msg)

if __name__ == "__main__":
    # ✅ FIXED: Read debug mode from environment variable
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
