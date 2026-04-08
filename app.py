from flask import Flask, render_template, request, redirect, session
import psycopg2
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# 🔐 SECRET KEY
app.secret_key = "mysecretkey123"

# ☁️ CLOUDINARY (DIRECT)
cloudinary.config(
    cloud_name="dr0hbtyqz",
    api_key="561717122881691",
    api_secret="8YDRpIY46-_X2bca6DLMoOs-qAI"
)

# ======================
# 🔌 DATABASE (DIRECT)
# ======================
def get_db_connection():
    return psycopg2.connect(
        "postgresql://ny_sariko_user:UcqLatZMNCQkVNMDKnVpcCXRp4Tw1kov@dpg-d772v5450q8c73ds9la0-a/ny_sariko",
        sslmode="require"
    )

# ======================
# 🏠 PUBLIC
# ======================
@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS media (
        id SERIAL PRIMARY KEY,
        nom TEXT,
        url TEXT,
        type TEXT,
        description TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id SERIAL PRIMARY KEY,
        media_id INTEGER,
        text TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS likes (
        id SERIAL PRIMARY KEY,
        media_id INTEGER
    )
    """)

    cursor.execute("SELECT * FROM media ORDER BY id DESC")
    medias = cursor.fetchall()

    cursor.execute("SELECT * FROM comments")
    comments = cursor.fetchall()

    cursor.execute("SELECT media_id, COUNT(*) FROM likes GROUP BY media_id")
    likes_data = cursor.fetchall()

    likes = {m[0]: 0 for m in medias}
    for l in likes_data:
        likes[l[0]] = l[1]

    conn.close()

    return render_template("index.html", medias=medias, comments=comments, likes=likes)

# ❤️ LIKE
@app.route("/like/<int:id>")
def like(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO likes (media_id) VALUES (%s)", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

# 🔐 LOGIN
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "maFamille" and request.form["password"] == "falyst##123":
            session["admin"] = True
            return redirect("/admin")
        else:
            return render_template("login.html", error="Diso ny code")

    return render_template("login.html")

# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ⚙️ ADMIN
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM media ORDER BY id DESC")
    medias = cursor.fetchall()
    conn.close()

    return render_template("admin.html", medias=medias)

# 📤 UPLOAD
@app.route("/upload", methods=["POST"])
def upload():
    if not session.get("admin"):
        return redirect("/login")

    file = request.files["file"]
    description = request.form.get("description")

    result = cloudinary.uploader.upload(file, resource_type="auto")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO media (nom, url, type, description) VALUES (%s,%s,%s,%s)",
        (file.filename, result["secure_url"], result["resource_type"], description)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")

# ❌ DELETE
@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("admin"):
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM media WHERE id=%s",(id,))
    conn.commit()
    conn.close()

    return redirect("/admin")

# 💬 COMMENT
@app.route("/comment", methods=["POST"])
def comment():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO comments (media_id,text) VALUES (%s,%s)",
        (request.form["media_id"], request.form["text"])
    )

    conn.commit()
    conn.close()

    return redirect("/")