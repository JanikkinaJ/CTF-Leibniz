from flask import Flask, send_from_directory, request, render_template
app = Flask(__name__)

@app.route("/")
def hello_world():
    return send_from_directory('static', 'index.html')

@app.route('/admin.html', methods=['GET', 'POST'])
def login_post():
   if request.method == 'POST':
        return login_logic()
   else:
        return render_template('admin.html', error=None)

@app.route('/<filename>')
def serve_file(filename):
    return send_from_directory('static', filename)

def login_logic():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return "valid login :D"
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('admin.html', error=error)

def valid_login(name, password):
    if name == "admin" and password == "password":
        return True
    return False

