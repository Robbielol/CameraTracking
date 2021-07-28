from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("Login.html")


@app.route("/MainCamera.html", methods=['post', 'get'])
def mainCamera():
    return render_template("MainCamera.html", title='Main')


@app.route("/Faces.html")
def facesPage():
    return render_template("Faces.html", title='Faces')


@app.route("/Recordings.html")
def RecordingsPage():
    return render_template("Recordings.html", title='Recordings')


if __name__ == '__main__':
    app.debug = True
    app.run()
