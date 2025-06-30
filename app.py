from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Question Model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # A, B, C, D

# Home route to show quiz
@app.route('/')
def quiz():
    questions = Question.query.all()
    return render_template('quiz.html', questions=questions)

# Route to handle quiz submission
@app.route('/submit', methods=['POST'])
def submit():
    questions = Question.query.all()
    score = 0
    total = len(questions)

    for question in questions:
        selected = request.form.get(str(question.id))
        if selected == question.correct_option:
            score += 1

    return render_template('result.html', score=score, total=total)

# Run the app and create tables
if __name__ == '_main_':
    with app.app_context():
        db.create_all()  # This creates the database file and table if not exists
    app.run(debug=True)


