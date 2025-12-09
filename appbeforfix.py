from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# intentionally vulnerable login route (SQL injection)
@app.route("/", methods=["GET", "POST"])
def home():
    msg = ""
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
# with SQL injection 
        conn = sqlite3.connect("app.db")
        cur = conn.cursor()
        query = f"SELECT * FROM users WHERE username='{user}' AND password='{pwd}'"
        cur.execute(query)



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
    app.run(debug=False)




