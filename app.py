from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, date
import sqlite3

app = Flask(_name_)
CORS(app)

DB = 'greetings.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS greetings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipient TEXT,
        sender TEXT,
        message TEXT,
        created_at TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/age')
def age():
    dob = request.args.get('dob')
    if not dob:
        return jsonify(error='dob param missing'), 400
    b = datetime.strptime(dob, '%Y-%m-%d').date()
    today = date.today()
    age = today.year - b.year - ((today.month, today.day) < (b.month, b.day))
    return jsonify(dob=dob, age=age)

@app.route('/greetings', methods=['POST'])
def save_greeting():
    data = request.get_json() or {}
    recipient = data.get('to') or 'Doanh'
    sender = data.get('from') or 'Bạn'
    message = data.get('message') or ''
    created = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('INSERT INTO greetings (recipient, sender, message, created_at) VALUES (?,?,?,?)',
              (recipient, sender, message, created))
    conn.commit()
    conn.close()
    return jsonify(status='ok', recipient=recipient)

@app.route('/list')
def list_greetings():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT id, recipient, sender, message, created_at FROM greetings ORDER BY id DESC LIMIT 50')
    rows = c.fetchall()
    conn.close()
    results = []
    for r in rows:
        results.append({'id': r[0], 'recipient': r[1], 'sender': r[2], 'message': r[3], 'created_at': r[4]})
    return jsonify(results)

if _name_ == '_main_':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)