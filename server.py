import os
import re
from flask import Flask, Response, redirect, render_template, request, send_file

# KHJAI-49324 camera server
# CTFUA{*****_cr4ppy_*****_********}
app = Flask(__name__)

def verify_credentials(username, password):
    regex   = re.compile('^' + username + ':' + password + '$')

    with open('./credentials.txt', 'r') as f:
        line = f.readline()

        return regex.match(line)

@app.route('/favicon.ico')
def favicon():
    return send_file('./favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def serve_feed():
    return render_template('camera.html')

@app.route('/admin', methods=['GET'])
def admin():
    auth = request.authorization

    if auth and verify_credentials(auth.username, auth.password):
        static_dir = os.path.join(app.root_path, 'static')
        files = os.listdir(static_dir)
        return render_template('admin.html', files=files)
    else:
        return Response('The credentials provided to access the KHJAI-49324 camera are incorrect.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route('/admin', methods=['POST'])
def download_file():
    auth = request.authorization

    if not auth or not verify_credentials(auth.username, auth.password):
        return Response('The credentials provided to access the KHJAI-49324 camera are incorrect.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    filename = request.form.get("filename").replace("../","")
    if filename:
        try:
            return send_file('./static/' + filename, as_attachment=True)
        except FileNotFoundError:
            return redirect("/admin")
    else:
        return redirect("/admin")

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')



