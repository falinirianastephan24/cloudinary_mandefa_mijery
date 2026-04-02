# =========================
# APP FLASK FINAL (VERSION STABLE HO AN'NY RENDER)
# =========================

from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# =========================
# 🔗 CONNECTION POSTGRESQL
# =========================
def get_db_connection():
    return psycopg2.connect(
        "postgresql://ny_sariko_user:UcqLatZMNCQkVNMDKnVpcCXRp4Tw1kov@dpg-d772v5450q8c73ds9la0-a/ny_sariko",
        sslmode="require"
    )

# =========================
# 🗃️ CREATE TABLE RAHA TSY MISY
# =========================
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

# =========================
# 🚀 ATAO REHEFA MISY REQUEST VOALOHANY
# (zava-dehibe ho an'ny Render)
# =========================
@app.before_first_request
def setup():
    try:
        init_db()
        print("✅ Database OK")
    except Exception as e:
        print("❌ Erreur DB:", e)

# =========================
# 🏠 PAGE PRINCIPALE
# =========================
@app.route("/")
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM media ORDER BY id DESC")
        medias = cursor.fetchall()

        conn.close()

        return render_template("index.html", medias=medias)

    except Exception as e:
        return f"❌ Erreur affichage: {e}"

# =========================
# 💾 SAVE DATA AVY AMIN'NY JAVASCRIPT
# =========================
@app.route("/save", methods=["POST"])
def save():
    try:
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

    except Exception as e:
        return jsonify({"error": str(e)})

# =========================
# ❌ DELETE MEDIA
# =========================
@app.route("/delete/<int:id>")
def delete(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM media WHERE id=%s", (id,))

        conn.commit()
        conn.close()

        return jsonify({"status": "deleted"})

    except Exception as e:
        return jsonify({"error": str(e)})

# =========================
# 🚀 FANDEHANA (LOCAL ONLY)
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)