from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
import hashlib
import json
import os
import re

app = Flask(__name__)

def load_logins():
    if os.path.exists("logins.json"):
        with open("logins.json", "r") as file:
            return json.load(file)
    return {}

def save_logins(data):
    with open("logins.json", "w") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        encrypted_email = hashlib.sha256(email.encode()).hexdigest()
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        users = load_logins()
        if encrypted_email in users and users[encrypted_email] == encrypted_password:
            return redirect('/dashboard')
        else:
            return "<h2>Login failed. ❌</h2><a href='/login'>Try again</a>"

    return render_template_string("""
        <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Login</title>
  <link rel="stylesheet" href="/login.css">
</head>
<body>
  <div class="form-box">
    <form method="POST">
      <h2>Login</h2>
      <input type="text" name="email" placeholder="Email" required><br>
      <input type="password" name="password" placeholder="Password" required><br>
      <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href="/register">Register here</a></p>
  </div>
</body>
</html>
    """)


@app.route("/dashboard")
def dashboard():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>User Dashboard</title>
      <link rel="stylesheet" href="/main.css">
    </head>
    <body>
      <div class="dashboard-container">
        <h1>Solitaire Collections</h1>
        <p>Level 1</p>
        <div>
          <button class="buttonn" onclick="startGame('index.html')">Play Solitaire</button>
          <button class="buttonn" onclick="startGame('hunt.html')">Play Hunt the Ace</button>
        </div>
      </div>

      <script>
        const name = localStorage.getItem('name');
        const level = localStorage.getItem('level');

        document.getElementById('greeting').textContent = `Hello, ${name || 'Player'}!`;
        document.getElementById('userLevel').textContent = `Level: ${level || '1'}`;

        function startGame(page) {
          window.location.href = page;
        }
      </script>
    </body>
    </html>
    """)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["first_name"]
        surname = request.form["last_name"]
        password = request.form["password"]
        
        if len(name) < 3 or len(surname) < 3:
            return "<h2>Name and surname must be at least 3 characters.</h2><a href='/register'>Back</a>"

        if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"\d", password):
            return "<h2>Password must be strong (8+ chars, upper, lower, number).</h2><a href='/register'>Back</a>"

        email = f"{name.lower()}.{surname.lower()}{os.urandom(2).hex()}@gmail.com"
        encrypted_email = hashlib.sha256(email.encode()).hexdigest()
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        users = load_logins()
        users[encrypted_email] = encrypted_password
        save_logins(users)

        return f"<h2>Account created! Your email: <strong>{email}</strong></h2><a href='/login'>Login now</a>"

    return render_template_string("""
        <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Register</title>
  <link rel="stylesheet" href="/register.css">
</head>
<body>
    <div class="form-box">
    <form method="post">
    <h2>Register</h2>
        <input type="text" name="first_name" placeholder="First Name" required><br>
        <input type="text" name="last_name" placeholder="Last Name" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <input type="submit" value="Register">
    </form>
    <p>Already have an account? <a href="/login">Login here</a></p>
</div>
</body>
</html>
    """)

# Route to serve login.css
@app.route("/login.css")
def serve_login_css():
    return send_from_directory(".", "login.css")

# Route to serve register.css
@app.route("/register.css")
def serve_register_css():
    return send_from_directory(".", "register.css")

# Route to serve images (optional)
@app.route("/images/<path:filename>")
def serve_images(filename):
    return send_from_directory("images", filename)

@app.route("/logins.js")
def serve_js():
    return send_from_directory(".", "logins.js")

@app.route("/main.css")
def serve_main_css():
    return send_from_directory(".", "main.css")

@app.route("/index.html")
def serve_index_html():
    return send_from_directory(".", "index.html")

@app.route("/style.css")
def serve_index_css():
    return send_from_directory(".", "style.css")

@app.route("/script.js")
def serve_index_js():
    return send_from_directory(".", "script.js")

@app.route("/hunt.html")
def serve_hunt_html():
    return send_from_directory(".", "hunt.html")

@app.route("/hunt.css")
def serve_hunt_css():
    return send_from_directory(".", "hunt.css")

@app.route("/index.js")
def serve_hunt_js():
    return send_from_directory(".", "index.js")

if __name__ == "__main__":
    app.run(debug=True)
