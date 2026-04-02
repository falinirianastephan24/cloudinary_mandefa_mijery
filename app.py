# =========================
# APP FLASK FINAL (NO CRASH VERSION)
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
# 🏠 PAGE PRINCIPALE
# =========================
@app.route("/")
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # atao create table eto (safe)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS media (
                id SERIAL PRIMARY KEY,
                nom TEXT,
                url TEXT,
                type TEXT
            )
        """)

        cursor.execute("SELECT * FROM media ORDER BY id DESC")
        medias = cursor.fetchall()

        conn.commit()
        conn.close()

        return render_template("index.html", medias=medias)

    except Exception as e:
        return f"❌ ERREUR SERVER: {e}"

# =========================
# 💾 SAVE DATA
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
# ❌ DELETE
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
# 🚀 LOCAL ONLY
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)