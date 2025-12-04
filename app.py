import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# -----------------------------
# MySQL CONFIG FOR YOUR SYSTEM
# -----------------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'          # your MySQL username
app.config['MYSQL_PASSWORD'] = 'azad'      # your MySQL password
app.config['MYSQL_DB'] = 'mydb'            # YOUR DATABASE NAME

# Initialize MySQL
mysql = MySQL(app)

# -----------------------------
# Table create karne ki zaroorat nahi
# Kyunki table 'messages' already exists
# -----------------------------
def init_db():
    pass   # Do nothing

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')   # your table name
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': new_message})

# -----------------------------
# Run app
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
