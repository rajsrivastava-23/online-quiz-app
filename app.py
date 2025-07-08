import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- Check if database exists, else create ---
if not os.path.exists('database.db'):
    print("Database not found. Creating now...")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            option4 TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')
    sample_questions = [
        ("What is the capital of India?", "Mumbai", "Delhi", "Kolkata", "Chennai", "Delhi"),
        ("Who wrote Ramayana?", "Valmiki", "Tulsidas", "Kalidas", "Ved Vyas", "Valmiki"),
        ("Which planet is known as Red Planet?", "Earth", "Mars", "Jupiter", "Venus", "Mars")
    ]
    cursor.executemany('''
        INSERT INTO questions (question, option1, option2, option3, option4, answer)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_questions)
    conn.commit()
    conn.close()
    print("Database created with sample questions!")
else:
    print("Database already exists. Skipping creation.")

# --- Flask Routes ---
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    conn.close()
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    conn.close()
    for q in questions:
        user_answer = request.form.get(str(q[0]))
        if user_answer == q[6]:  # q[6] is correct answer
            score += 1
    return render_template('result.html', score=score, total=len(questions))

if __name__ == '__main__':
    app.run(debug=True)