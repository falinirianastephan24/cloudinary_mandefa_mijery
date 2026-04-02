# =========================
# APP FLASK FINAL (RENDER + POSTGRESQL OK)
# =========================

from flask import Flask, render_template, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# =========================
# 🔗 CONNECTION POSTGRESQL (AVY AMIN'NY ENV)
# =========================
def get_db_connection():
    try:
        return psycopg2.connect(
            os.environ.get("DATABASE_URL"),
            sslmode="require"
        )
    except Exception as e:
        print("❌ ERREUR DB:", e)
        return None

# =========================
# 🏠 PAGE PRINCIPALE
# =========================
@app.route("/")
def index():
    conn = get_db_connection()

    # ❗ Raha tsy connect DB
    if conn is None:
        return "⚠️ TSY MI-CONNECT NY DATABASE (jereo Render → Environment)"

    try:
        cursor = conn.cursor()

        # 🗃️ CREATE TABLE RAHA TSY MISY
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS media (
                id SERIAL PRIMARY KEY,
                nom TEXT,
                url TEXT,
                type TEXT
            )
        """)

        # 📥 Maka data
        cursor.execute("SELECT * FROM media ORDER BY id DESC")
        medias = cursor.fetchall()

        conn.commit()
        conn.close()

        return render_template("index.html", medias=medias)

    except Exception as e:
        return f"❌ ERREUR DATABASE: {e}"

# =========================
# 💾 SAVE DATA (AVY AMIN'NY JS)
# =========================
@app.route("/save", methods=["POST"])
def save():
    conn = get_db_connection()

    if conn is None:
        return jsonify({"error": "DB TSY CONNECT"})

    try:
        data = request.get_json()
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
    conn = get_db_connection()

    if conn is None:
        return jsonify({"error": "DB TSY CONNECT"})

    try:
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