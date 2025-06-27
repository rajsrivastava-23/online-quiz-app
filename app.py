from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# 🔐 API Key for protected API route
API_KEY = "mysecretapikey123"  # change this to something secret

# 🏠 Home Page
@app.route('/')
def home():
    return render_template('index.html')


# ❓ Quiz Page
@app.route('/quiz')
def quiz():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions')
    questions = cursor.fetchall()
    conn.close()
    return render_template('quiz.html', questions=questions)


# 📤 Submit Quiz and Show Result
@app.route('/submit', methods=['POST'])
def submit():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, correct_option FROM questions")
    correct_answers = {str(row[0]): row[1] for row in cursor.fetchall()}

    score = 0
    total = len(correct_answers)

    for q_id, correct_ans in correct_answers.items():
        selected = request.form.get(q_id)
        if selected == correct_ans:
            score += 1

    conn.close()
    return render_template('result.html', score=score, total=total)


# 🛠️ Admin Page to Add Questions
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        question = request.form['question']
        opt1 = request.form['opt1']
        opt2 = request.form['opt2']
        opt3 = request.form['opt3']
        opt4 = request.form['opt4']
        correct_option = request.form['correct']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO questions (question, opt1, opt2, opt3, opt4, correct_option)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (question, opt1, opt2, opt3, opt4, correct_option))
        conn.commit()
        conn.close()

        return redirect('/admin')

    return render_template('admin.html')


# 🌐 API Route with API Key Validation
@app.route('/api/questions')
def api_questions():
    key = request.args.get('key')

    if key != API_KEY:
        return jsonify({"error": "Unauthorized or invalid API key"}), 401

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, opt1, opt2, opt3, opt4 FROM questions")
    questions = cursor.fetchall()
    conn.close()

    result = []
    for q in questions:
        result.append({
            'id': q[0],
            'question': q[1],
            'options': [q[2], q[3], q[4], q[5]]
        })

    return jsonify(result)


# 🟢 Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)







