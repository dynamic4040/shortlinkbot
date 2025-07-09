from flask import Flask, request, redirect, jsonify
import sqlite3, string, random

app = Flask(__name__)
@app.route('/ping')
def ping():
    return "pong"
conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cur = conn.cursor()

# Create table
cur.execute('''
CREATE TABLE IF NOT EXISTS links (
    code TEXT PRIMARY KEY,
    url TEXT,
    clicks INTEGER DEFAULT 0,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.form.get('url')
    print("Received URL:", url)
    custom = request.form.get('custom')
    
    if not url:
        return "Missing URL", 400
    
    code = custom if custom else generate_code()
    
    cur.execute("SELECT * FROM links WHERE code=?", (code,))
    if cur.fetchone() and not custom:
        code = generate_code()
    
    cur.execute("INSERT OR REPLACE INTO links (code, url, clicks) VALUES (?, ?, 0)", (code, url))
    conn.commit()
    
    return f"http://localhost:5000/{code}"

@app.route('/<code>')
def redirect_link(code):
    cur.execute("SELECT url FROM links WHERE code=?", (code,))
    result = cur.fetchone()
    
    if result:
        cur.execute("UPDATE links SET clicks = clicks + 1 WHERE code=?", (code,))
        conn.commit()
        return redirect(result[0])
    
    return "Link not found", 404

@app.route('/stats/<code>')
def stats(code):
    cur.execute("SELECT url, clicks, created FROM links WHERE code=?", (code,))
    data = cur.fetchone()
    if data:
        return jsonify({
            "original_url": data[0],
            "clicks": data[1],
            "created": data[2]
        })
    return jsonify({"error": "Link not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
