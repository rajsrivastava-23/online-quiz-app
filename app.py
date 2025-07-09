from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Dummy data for quiz
quiz = [
    {"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin", "Madrid"], "answer": "Paris"},
    {"question": "Who wrote 'Hamlet'?", "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "J.K. Rowling"], "answer": "William Shakespeare"},
    {"question": "What is 5 + 7?", "options": ["10", "11", "12", "13"], "answer": "12"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz_page():
    return render_template('quiz.html', quiz=quiz)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    for i in range(len(quiz)):
        user_answer = request.form.get(f'question-{i}')
        if user_answer == quiz[i]['answer']:
            score += 1
    return redirect(url_for('result', score=score))

@app.route('/result')
def result():
    score = request.args.get('score')
    return render_template('result.html', score=score)

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)