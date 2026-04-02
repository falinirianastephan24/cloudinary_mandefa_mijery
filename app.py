# =========================
# app.py (VERSION AMIN'NY FANAZAVANA AMIN'NY TENY GASY)
# =========================

from flask import Flask, render_template, request, redirect
import psycopg2
import cloudinary
import cloudinary.uploader
import os

app = Flask(__name__)

# 🔐 CONFIG CLOUDINARY
# 👉 SOLOINAO amin'ny kaontinao manokana ireto
cloudinary.config(
    cloud_name="dr0hbtyqz",
    api_key="561717122881691",
    api_secret="8YDRpIY46-_X2bca6DLMoOs-qAI"
)

# 🔗 CONNECTION POSTGRESQL
# 👉 SOLOINAO amin'ny database-nao

def get_db_connection():
    return psycopg2.connect(
        "postgresql://ny_sariko_user:UcqLatZMNCQkVNMDKnVpcCXRp4Tw1kov@dpg-d772v5450q8c73ds9la0-a/ny_sariko",
        sslmode="require"
    )

# 🗃️ MAMORONA TABLE RAHA TSY MISY

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

# antsoina rehefa manomboka app
init_db()

# 🏠 PAGE PRINCIPALE
@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # maka ny media rehetra
    cursor.execute("SELECT * FROM media ORDER BY id DESC")
    medias = cursor.fetchall()

    conn.close()
    return render_template("index.html", medias=medias)

# 📤 UPLOAD FICHIER (IMAGE / VIDEO / ZIP / RAR / PDF)
@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")

    conn = get_db_connection()
    cursor = conn.cursor()

    for file in files:
        if file and file.filename != "":

            filename = file.filename
            ext = os.path.splitext(filename)[1].lower()

            # 📦 Raha ZIP / RAR / PDF
            if ext in [".zip", ".rar", ".pdf"]:
                result = cloudinary.uploader.upload(
                    file,
                    resource_type="raw"  # zava-dehibe!
                )
                resource_type = "raw"

            else:
                # 🖼️ na 🎥 (image/video)
                result = cloudinary.uploader.upload(file)
                resource_type = result["resource_type"]

            url = result["secure_url"]

            # 💾 Tehirizina ao anaty base de données
            cursor.execute(
                "INSERT INTO media (nom, url, type) VALUES (%s, %s, %s)",
                (filename, url, resource_type)
            )

    conn.commit()
    conn.close()

    return redirect("/")

# ❌ FAMAFANA MEDIA
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM media WHERE id=%s", (id,))

    conn.commit()
    conn.close()

    return redirect("/")

# 🚀 FANDEHANA NY APP
if __name__ == "__main__":
    app.run(debug=True)


# =========================

