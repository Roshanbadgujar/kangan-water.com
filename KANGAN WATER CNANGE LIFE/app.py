from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from functools import wraps
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure key
DATABASE = 'submissions.db'
UPLOAD_FOLDER = 'static/uploads/'
OWNER_USERNAME = 'Roshan Badgujar'
OWNER_PASSWORD = 'roshan777'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # Maximum file upload size is 16MB

def init_db():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS submissions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            phone TEXT NOT NULL,
                            email TEXT NOT NULL,
                            message TEXT NOT NULL
                          )''')
        conn.commit()
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS images (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            filename TEXT NOT NULL
                          )''')
        conn.commit()

init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('You need to log in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT filename FROM images')
        images = cursor.fetchall()
    return render_template('index.html', images=images)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    message = request.form['message']

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO submissions (name, phone, email, message) 
                          VALUES (?, ?, ?, ?)''', (name, phone, email, message))
        conn.commit()

    flash('Your submission has been received!')
    return redirect(url_for('index'))

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO images (filename) VALUES (?)''', (filename,))
            conn.commit()
        flash('Image successfully uploaded')
        return redirect(url_for('index'))

@app.route('/submissions')
@login_required
def view_submissions():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name, phone, email, message FROM submissions')
        submissions = cursor.fetchall()
    return render_template('submissions.html', submissions=submissions)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == OWNER_USERNAME and password == OWNER_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('view_submissions'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
