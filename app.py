from flask import Flask, render_template, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# =========================
# DB CONNECTION
# =========================
def get_db_connection():
    try:
        return psycopg2.connect(
            os.environ.get("DATABASE_URL"),
            sslmode="require"
        )
    except Exception as e:
        print("DB ERROR:", e)
        return None

# =========================
# HOME
# =========================
@app.route("/")
def index():
    conn = get_db_connection()

    if conn is None:
        return "DB TSY CONNECT"

    cursor = conn.cursor()

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

# =========================
# SAVE
# =========================
@app.route("/save", methods=["POST"])
def save():
    conn = get_db_connection()

    if conn is None:
        return jsonify({"error": "DB ERROR"})

    try:
        data = request.get_json() or {}

        # SAFE TYPE
        type_value = data.get("type") or "raw"

        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO media (nom, url, type) VALUES (%s, %s, %s)",
            (data.get("nom"), data.get("url"), type_value)
        )

        conn.commit()
        conn.close()

        return jsonify({"status": "ok"})

    except Exception as e:
        return jsonify({"error": str(e)})

# =========================
# DELETE
# =========================
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()

    if conn is None:
        return jsonify({"error": "DB ERROR"})

    cursor = conn.cursor()
    cursor.execute("DELETE FROM media WHERE id=%s", (id,))

    conn.commit()
    conn.close()

    return jsonify({"status": "deleted"})

# =========================
# RUN LOCAL
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)