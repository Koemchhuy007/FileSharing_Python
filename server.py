from flask import Flask, request, render_template_string, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "FileSharing"

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
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    text-align: center;
                }
                textarea {
                    width: 100%;
                    height: 60vh;
                    font-size: 16px;
                }
                button, input[type="file"] {
                    font-size: 18px;
                    padding: 10px 20px;
                    margin: 10px;
                    width: 100%;
                    max-width: 300px;
                }
            </style>
        </head>
        <body>
            <form method="post" action="/save">
                <textarea name="content">{{ content }}</textarea>
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

@app.route('/files', methods=['GET', 'POST'])
def list_files():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded. <a href='/files'>Go back</a>"
        file = request.files['file']
        if file.filename == '':
            return "No selected file. <a href='/files'>Go back</a>"
        file.save(os.path.join(FILE_DIR, file.filename))
    
    files = os.listdir(FILE_DIR)
    return render_template_string('''
        <html>
        <head>
            <title>File Sharing</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    text-align: center;
                }
                ul {
                    list-style: none;
                    padding: 0;
                }
                li {
                    margin: 10px 0;
                }
                a {
                    text-decoration: none;
                    color: blue;
                }
                button, input[type="file"] {
                    font-size: 18px;
                    padding: 10px 20px;
                    margin: 10px;
                    width: 100%;
                    max-width: 300px;
                }
            </style>
        </head>
        <body>
            <h1>File Sharing</h1>
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <button type="submit">Upload</button>
            </form>
            <ul>
                {% for file in files %}
                    <li><a href="/download/{{ file }}" download>{{ file }}</a></li>
                {% endfor %}
            </ul>
        </body>
        </html>
    ''', files=files)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(FILE_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)