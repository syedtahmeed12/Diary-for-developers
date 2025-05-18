import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Fetch all notes
def get_notes():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM notes")
    notes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return notes

# Add a new note
def add_note_to_db(note):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (content) VALUES (?)", (note,))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html', notes=get_notes())

@app.route('/add', methods=['POST'])
def add_note():
    note = request.form.get('note')
    if note:
        add_note_to_db(note)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
