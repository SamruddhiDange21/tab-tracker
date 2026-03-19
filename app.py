from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # makes data easier to use
    return conn


# -------------------------------
# INITIALIZE DATABASE
# -------------------------------
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tabs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            reason TEXT NOT NULL,
            category TEXT,
            time TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# -------------------------------
# ROUTES
# -------------------------------

# Home Page
@app.route('/')
def index():
    return render_template("index.html")


# Save Tab Data
@app.route('/save', methods=['POST'])
def save():
    url = request.form.get('url')
    reason = request.form.get('reason')

    # basic validation (don’t skip this)
    if not url or not reason:
        return "Missing data", 400

    # simple category logic (upgrade later)
    if "youtube" in url.lower():
        category = "Entertainment"
    elif "leetcode" in url.lower():
        category = "Learning"
    else:
        category = "Other"

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tabs (url, reason, category, time) VALUES (?, ?, ?, ?)",
        (url, reason, category, time)
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')


# Dashboard View
@app.route('/dashboard')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tabs ORDER BY time DESC")
    data = cursor.fetchall()

    conn.close()

    return render_template("dashboard.html", data=data)


# -------------------------------
# INSIGHTS (IMPORTANT FEATURE)
# -------------------------------
@app.route('/insights')
def insights():
    conn = get_db()
    cursor = conn.cursor()

    # Most visited site
    cursor.execute('''
        SELECT url, COUNT(*) as count 
        FROM tabs 
        GROUP BY url 
        ORDER BY count DESC 
        LIMIT 1
    ''')
    top_site = cursor.fetchone()

    # Category usage
    cursor.execute('''
        SELECT category, COUNT(*) as count
        FROM tabs
        GROUP BY category
    ''')
    categories = cursor.fetchall()

    conn.close()

    return render_template("insights.html", 
                           top_site=top_site, 
                           categories=categories)


# -------------------------------
# DELETE ENTRY (optional but useful)
# -------------------------------
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tabs WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect('/dashboard')


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)