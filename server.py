from flask import Flask, request, render_template_string, send_from_directory
import os

app = Flask(__name__)

NOTE_FILE = "note.html"
FILE_DIR = "FileSharing"

# Ensure the file and directory exist
if not os.path.exists(NOTE_FILE):
    with open(NOTE_FILE, "w") as f:
        f.write("<h1>Welcome to Your Note</h1><p>Edit this text.</p>")

if not os.path.exists(FILE_DIR):
    os.makedirs(FILE_DIR)

@app.route('/')
def index():
    with open(NOTE_FILE, "r") as f:
        content = f.read()
    return render_template_string('''
        <html>
        <head>
            <title>Note Editor</title>
            <style>
                button {
                    font-size: 20px;
                    padding: 10px 20px;
                    margin: 10px;
                }
            </style>
        </head>
        <body>
            <form method="post" action="/save">
                <textarea name="content" style="width:100%; height:80vh;">{{ content }}</textarea>
                <br>
                <button type="submit">Save</button>
                <a href="/files"><button type="button">Go to File Sharing</button></a>
            </form>
        </body>
        </html>
    ''', content=content)

@app.route('/save', methods=['POST'])
def save():
    content = request.form['content']
    with open(NOTE_FILE, "w") as f:
        f.write(content)
    return "<p>Saved! <a href='/'>Go back</a></p>"

@app.route('/files')
def list_files():
    files = os.listdir(FILE_DIR)
    return render_template_string('''
        <html>
        <head><title>File Sharing</title></head>
        <body>
            <h1>File Sharing</h1>
            <ul>
                {% for file in files %}
                    <li><a href="/files/{{ file }}">{{ file }}</a></li>
                {% endfor %}
            </ul>
        </body>
        </html>
    ''', files=files)

@app.route('/files/<path:filename>')
def download_file(filename):
    return send_from_directory(FILE_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
