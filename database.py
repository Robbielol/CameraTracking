from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Data(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)

    def __init__(self, id, username):
        self.id = id
        self.username = username


    def getUser(self, username):
        return db.engine.execute(
            "SELECT username FROM users WHERE username='" + username + "'")
