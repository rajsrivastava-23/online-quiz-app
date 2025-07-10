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
    if request.method == 'POST':
        return redirect(url_for('submit'))
    return render_template('quiz.html', quiz=quiz)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    total = len(quiz)

    for i, question in enumerate(quiz, start=1):
        user_answer = request.form.get(f'question-{i}')

        # ✅ Add this validation to catch empty answers
        if not user_answer:
            return f"Please select an option for Question {i}", 400

        if user_answer == question['answer']:
            score += 1

    return render_template('result.html', score=score, total=total)

@app.route('/result')
def result():
    return redirect(url_for('quiz_page'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)