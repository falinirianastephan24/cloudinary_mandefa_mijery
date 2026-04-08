from flask import Flask, render_template, request, redirect, session
import psycopg2
import os
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# 🔐 key an'ny session
app.secret_key = "SECRET_KEY"

# ☁️ config Cloudinary
cloudinary.config(
    cloud_name="dr0hbtyqz",
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET"
)

# =========================
# 🔌 connexion database
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
# 🏠 page principale
# =========================
@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # table media
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media (
            id SERIAL PRIMARY KEY,
            nom TEXT,
            url TEXT,
            type TEXT,
            description TEXT
        )
    """)

    # table commentaire
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
# 🔐 login (popup)
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # 🔑 ovay eto ny code-nao
        if username == "maFamille" and password == "falyst##123":
            session["admin"] = True

            # mihidy popup + refresh page
            return "<script>window.opener.location.reload(); window.close();</script>"
        else:
            return render_template("login.html", error="❌ Diso ny code")

    return render_template("login.html")

# =========================
# 🚪 logout
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# =========================
# 📤 upload (admin ihany)
# =========================
@app.route("/upload", methods=["POST"])
def upload():
    if not session.get("admin"):
        return "❌ Tsy mahazo upload raha tsy admin"

    file = request.files["file"]
    description = request.form.get("description")

    result = cloudinary.uploader.upload(file, resource_type="auto")

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
# ❌ delete (admin ihany)
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
# 💬 commentaire
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
# ▶️ lancement
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)