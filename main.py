from flask import Flask, render_template, request, session, redirect, url_for
from database import db

app = Flask(__name__)
app.secret_key = "secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/Camera_Tracking'

db.init_app(app)

loggedIn = False


@app.route("/")
def login():
    return render_template("Login.html")


@app.route("/Proxy.html", methods=['POST', 'GET'])
def proxy():
    username: str = request.form["username"]
    session['username'] = username
    login_authorization(username, "MainCamera.html", 'Main')
    return redirect(url_for("mainCamera"))
    #return login_authorization(username, "MainCamera.html", 'Main')


@app.route("/MainCamera.html", methods=['POST', 'GET'])
def mainCamera():
    username = session['username']
    return login_authorization(username, "MainCamera.html", 'Main')


@app.route("/Faces.html")
def facesPage():
    username = session['username']
    return login_authorization(username, "Faces.html", 'Faces ')


@app.route("/Recordings.html")
def RecordingsPage():
    username = session['username']
    return login_authorization(username, "Recordings.html", 'Recordings')


def login_authorization(username, htmlPage, pageTitle):
    result = db.engine.execute(
        "SELECT username FROM users WHERE username='" + username + "'")# returns cursorResult object
    if result.rowcount > 0:
        result_username = result.first()[0]  # result rows are returned as tuples
        if username != result_username:
            return render_template("Login.html")
        else:
            return render_template(htmlPage, title=pageTitle)
    else:
        return render_template("Login.html")


if __name__ == '__main__':
    app.debug = True
    print("hi")
    app.run()
