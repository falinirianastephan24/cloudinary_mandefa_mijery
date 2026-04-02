# =========================
# APP FLASK - UPLOAD MEDIA (VERSION HAINGANA)
# =========================

from flask import Flask, render_template, request, redirect
import psycopg2
import cloudinary
import cloudinary.uploader
import os

app = Flask(__name__)

# 🔐 CONFIG CLOUDINARY
# 👉 SOLOINAO amin'ny kaontinao
cloudinary.config(
    cloud_name="dr0hbtyqz",
    api_key="561717122881691",
    api_secret="8YDRpIY46-_X2bca6DLMoOs-qAI"
)

# 🔗 CONNECTION POSTGRESQL
def get_db_connection():
    return psycopg2.connect(
        "postgresql://ny_sariko_user:UcqLatZMNCQkVNMDKnVpcCXRp4Tw1kov@dpg-d772v5450q8c73ds9la0-a/ny_sariko",
        sslmode="require"
    )

# 🗃️ CREATE TABLE
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media (
            id SERIAL PRIMARY KEY,
            nom TEXT,
            url TEXT,
            type TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# 🏠 PAGE PRINCIPALE
@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM media ORDER BY id DESC")
    medias = cursor.fetchall()

    conn.close()
    return render_template("index.html", medias=medias)

# 📤 UPLOAD FICHIER (VERSION HAINGANA)
@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")

    conn = get_db_connection()
    cursor = conn.cursor()

    for file in files:
        if file and file.filename != "":

            # ⚠️ LIMIT SIZE (20MB max)
            if file.content_length and file.content_length > 20 * 1024 * 1024:
                continue  # tsy alefa raha lehibe loatra

            # 🚀 UPLOAD HAINGANA (AUTO + CHUNK)
            result = cloudinary.uploader.upload(
                file,
                resource_type="auto",     # mahita ho azy (image/video/raw)
                chunk_size=6000000        # tsara ho an'ny gros fichier
            )

            url = result["secure_url"]
            resource_type = result["resource_type"]

            # 💾 INSERT DB
            cursor.execute(
                "INSERT INTO media (nom, url, type) VALUES (%s, %s, %s)",
                (file.filename, url, resource_type)
            )

    conn.commit()
    conn.close()

    return redirect("/")

# ❌ DELETE
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM media WHERE id=%s", (id,))

    conn.commit()
    conn.close()

    return redirect("/")

# 🚀 RUN
if __name__ == "__main__":
    app.run(debug=True)