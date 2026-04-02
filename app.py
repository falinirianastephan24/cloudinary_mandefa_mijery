from flask import Flask, render_template, request, redirect
import sqlite3
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# 🔐 CONFIG CLOUDINARY
cloudinary.config(
    cloud_name="dr0hbtyqz",
    api_key="561717122881691",
    api_secret="8YDRpIY46-_X2bca6DLMoOs-qAI"
)

# 🗃️ INIT DB
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            image_url TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# 🏠 HOME
@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM images")
    images = cursor.fetchall()

    conn.close()
    return render_template("index.html", images=images)

# 📤 UPLOAD
@app.route("/upload", methods=["POST"])
def upload():
    nom = request.form["nom"]
    file = request.files["image"]

    image_url = None

    if file and file.filename != "":
        result = cloudinary.uploader.upload(file)
        image_url = result["secure_url"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO images (nom, image_url) VALUES (?, ?)",
        (nom, image_url)
    )

    conn.commit()
    conn.close()

    return redirect("/")

# ❌ DELETE
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM images WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)