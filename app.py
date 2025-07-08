from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Function to get questions from database
def get_questions():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, option1, option2, option3, option4, answer FROM questions")
    rows = cursor.fetchall()
    conn.close()

    questions = []
    for row in rows:
        questions.append({
            'id': row[0],
            'question': row[1],
            'options': [row[2], row[3], row[4], row[5]],
            'answer': row[6]
        })
    return questions

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/quiz")
def quiz():
    questions = get_questions()
    session['questions'] = questions
    session['current_question'] = 0
    session['score'] = 0
    return render_template("quiz.html", question=questions[0], qno=1)

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    selected_option = request.form.get("option")
    qno = session.get('current_question')
    questions = session.get('questions')
    score = session.get('score')

    correct_answer = questions[qno]['answer']
    if selected_option == correct_answer:
        session['score'] = score + 1

    qno += 1
    session['current_question'] = qno

    if qno < len(questions):
        return render_template("quiz.html", question=questions[qno], qno=qno+1)
    else:
        return redirect(url_for('result'))

@app.route("/result")
def result():
    score = session.get('score')
    total = len(session.get('questions'))
    return render_template("result.html", score=score, total=total)

if __name__ == "__main__":
    app.run(debug=True)


 