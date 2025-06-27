import sqlite3

# Step 1: Database se connect karo (file ban jaayegi agar nahi hai)
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Step 2: Table create karo (agar pehle se nahi hai)
c.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    opt1 TEXT NOT NULL,
    opt2 TEXT NOT NULL,
    opt3 TEXT NOT NULL,
    opt4 TEXT NOT NULL,
    correct TEXT NOT NULL
)
''')

# Step 3: Ek sample question insert karo (optional)
sample_question = (
    "What is the capital of India?",
    "Mumbai",
    "Delhi",
    "Kolkata",
    "Chennai",
    "opt2"
)

c.execute("INSERT INTO questions (question, opt1, opt2, opt3, opt4, correct) VALUES (?, ?, ?, ?, ?, ?)", sample_question)

# Step 4: Changes save karo aur close karo
conn.commit()
conn.close()

print("✅ Database and table created successfully.")


