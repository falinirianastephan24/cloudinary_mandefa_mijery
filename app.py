# =========================
# APP FLASK FINAL (UPLOAD RAPIDE CLOUDINARY)
# =========================

from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# 🔗 CONNECTION POSTGRESQL (EFA FENO)
def get_db_connection():
    return psycopg2.connect(
        "postgresql://ny_sariko_user:UcqLatZMNCQkVNMDKnVpcCXRp4Tw1kov@dpg-d772v5450q8c73ds9la0-a/ny_sariko",
        sslmode="require"
    )

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

# antsoina rehefa manomboka
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

# 💾 SAVE DATA AVY AMIN'NY JAVASCRIPT
@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO media (nom, url, type) VALUES (%s, %s, %s)",
        (data["nom"], data["url"], data["type"])
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

# ❌ DELETE MEDIA
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM media WHERE id=%s", (id,))

    conn.commit()
    conn.close()

    return jsonify({"status": "deleted"})

# 🚀 MANDEHA NY APP
if __name__ == "__main__":
    app.run(debug=True)