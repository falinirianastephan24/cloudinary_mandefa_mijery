from flask import Flask, render_template, request, redirect, session
import psycopg2
import os
import cloudinary
import cloudinary.uploader

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

# ☁️ Cloudinary config
cloudinary.config(
    cloud_name="dr0hbtyqz",
    api_key="561717122881691",
    api_secret="8YDRpIY46-_X2bca6DLMoOs-qAI"
)

# =========================
# 🔌 DB CONNECTION
# =========================
def get_db_connection():
    try:
        return psycopg2.connect(
            os.environ.get("DATABASE_URL"),
            sslmode="require"
        )
    except:
        return None

# =========================
# 🏠 HOME
# =========================
@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 📁 media table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media (
            id SERIAL PRIMARY KEY,
            nom TEXT,
            url TEXT,
            type TEXT,
            description TEXT
        )
    """)

    # 💬 comment table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            media_id INTEGER,
            text TEXT
        )
    """)

    cursor.execute("SELECT * FROM media ORDER BY id DESC")
    medias = cursor.fetchall()

    cursor.execute("SELECT * FROM comments")
    comments = cursor.fetchall()

    conn.commit()
    conn.close()

    return render_template("index.html", medias=medias, comments=comments)

# =========================
# 🔐 LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "fammilleTojo" and password == "falyst##123":
            session["fammilleTojo"] = True
            return redirect("/")

    return render_template("login.html")

# =========================
# 🚪 LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# =========================
# 📤 UPLOAD (ADMIN ONLY)
# =========================
@app.route("/upload", methods=["POST"])
def upload():
    if not session.get("admin"):
        return redirect("/")

    file = request.files["file"]
    description = request.form.get("description")

    result = cloudinary.uploader.upload(file)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO media (nom, url, type, description) VALUES (%s, %s, %s, %s)",
        (file.filename, result["secure_url"], result["resource_type"], description)
    )

    conn.commit()
    conn.close()

    return redirect("/")

# =========================
# ❌ DELETE (ADMIN ONLY)
# =========================
@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("admin"):
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM media WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

# =========================
# 💬 COMMENT
# =========================
@app.route("/comment", methods=["POST"])
def comment():
    media_id = request.form["media_id"]
    text = request.form["text"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO comments (media_id, text) VALUES (%s, %s)",
        (media_id, text)
    )

    conn.commit()
    conn.close()

    return redirect("/")

# =========================
# ▶️ RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)