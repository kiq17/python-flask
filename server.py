from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from hash_table import HashTable

from linked_list import LinkedList

# app
app = Flask(__name__)
app.app_context().push()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0


# config sqlite

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


db = SQLAlchemy(app)
now = datetime.now()

# models


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost")


class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# routes


@app.route("/user", methods=["POST"])
def createUser():
    data = request.get_json()
    newUser = User(
        name=data["name"],
        email=data["email"],
        address=data["adress"],
        phone=data["phone"]
    )
    db.session.add(newUser)
    db.session.commit()

    return jsonify(data), 201


@app.route("/user/<user_id>", methods=["GET"])
def getUser(user_id):
    users = User.query.all()

    list = LinkedList()

    for user in users:
        list.inesertBegining(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )

    user = list.userById(user_id)
    return jsonify(user), 200


@app.route("/user/<user_id>", methods=["DELETE"])
def deleteUser(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()

    return jsonify({}), 204

@app.route("/post/<user_id>", methods=["POST"])
def createPost(user_id):
    data = request.get_json()

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message: user doesn't exits"})

    ht = HashTable(10)

    ht.addKeyValue("title", data["title"])
    ht.addKeyValue("body", data["body"])
    ht.addKeyValue("date", now)
    ht.addKeyValue("userId", user_id)

    newPost = BlogPost(
        title= ht.getValue("title"),
        body= ht.getValue("body"),
        date= ht.getValue("date"),
        user_id= ht.getValue("userId")
    )
    db.session.add(newPost)
    db.session.commit()

    return jsonify(data), 201

if __name__ == "__main__":
    app.run(debug=True)
