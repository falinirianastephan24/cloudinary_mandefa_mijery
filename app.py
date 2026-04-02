from flask import Flask, render_template, request, redirect
import psycopg2
import cloudinary
import cloudinary.uploader
import os

app = Flask(__name__)

# 🔐 CONFIG CLOUDINARY
cloudinary.config(
    cloud_name=os.getenv("dr0hbtyqz"),
    api_key=os.getenv("561717122881691"),
    api_secret=os.getenv("8YDRpIY46-_X2bca6DLMoOs-qAI")
)

# 🔗 CONNECTION POSTGRESQL
def get_db_connection():
    return psycopg2.connect(os.getenv("postgresql://ny_sariko_user:UcqLatZMNCQkVNMDKnVpcCXRp4Tw1kov@dpg-d772v5450q8c73ds9la0-a/ny_sariko"))

# 🗃️ CREATE TABLE RAHA TSY MISY
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

# 🏠 HOME
@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM media ORDER BY id DESC")
    medias = cursor.fetchall()

    conn.close()
    return render_template("index.html", medias=medias)

# 📤 UPLOAD SARY NA VIDEO MARO
@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")

    conn = get_db_connection()
    cursor = conn.cursor()

    for file in files:
        if file and file.filename != "":
            # Alefa any Cloudinary
            result = cloudinary.uploader.upload(file)

            url = result["secure_url"]

            # Fantarina hoe image sa video
            resource_type = result["resource_type"]  # image na video

            # 💾 Tehirizina ao DB
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

if __name__ == "__main__":
    app.run(debug=True)