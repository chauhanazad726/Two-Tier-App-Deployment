from flask import Flask, render_template, request, jsonify
import MySQLdb

app = Flask(__name__)

# -----------------------------
# DOCKER CONFIG
# -----------------------------
def get_db():
    return MySQLdb.connect(
        host="mysql",        # DOCKER MySQL container name
        user="root",
        passwd="azad",
        db="mydb"
    )

# -----------------------------
# HOME PAGE
# -----------------------------
@app.route('/')
def home():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT message FROM messages")
    messages = cur.fetchall()
    cur.close()
    db.close()
    return render_template('index.html', messages=messages)

# -----------------------------
# INSERT new message
# -----------------------------
@app.route('/submit', methods=['POST'])
def submit():
    msg = request.form.get('new_message')

    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO messages (message) VALUES (%s)", (msg,))
    db.commit()
    cur.close()
    db.close()

    return jsonify({"message": msg})

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
