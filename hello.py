from flask import Flask, send_from_directory
app = Flask(__name__)

@app.route("/")
def hello_world():
    return send_from_directory('static', 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('static', filename)
