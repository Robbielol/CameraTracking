from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("Login.html")


@app.route("/MainCamera.html", methods=['post'])
def mainCamera():
    return render_template("MainCamera.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
