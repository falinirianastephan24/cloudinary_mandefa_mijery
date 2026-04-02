from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# 🔗 CONNECTION DB (SAFE)
def get_db_connection():
    try:
        return psycopg2.connect(
            "postgresql://ny_sariko_user:UcqLatZMNCQkVNMDKnVpcCXRp4Tw1kov@dpg-d772v5450q8c73ds9la0-a/ny_sariko",
            sslmode="require"
        )
    except Exception as e:
        print("❌ DB CONNECTION ERROR:", e)
        return None

# 🏠 PAGE PRINCIPALE
@app.route("/")
def index():
    conn = get_db_connection()

    # raha tsy mandeha DB
    if conn is None:
        return "⚠️ DB TSY MI-CONNECT (jereo logs Render)"

    try:
        cursor = conn.cursor()

        # create table safe
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
        return f"❌ ERREUR DB: {e}"

# 💾 SAVE
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

# ❌ DELETE
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

# 🚀 LOCAL
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)