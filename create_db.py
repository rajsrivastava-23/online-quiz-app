import sqlite3

# Connect to SQLite database (or create if not exists)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table
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

# Insert sample data
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

print("Database and table created with sample questions ✅")