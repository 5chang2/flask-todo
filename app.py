from flask import Flask,render_template,request,redirect
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import datetime

from models import db, Todo

# app.py => sqlalchemy 설정
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db에 app 연동
db.init_app(app)

# migrations
migrate = Migrate(app,db)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos=todos)
    
@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    title = request.form["title"]
    deadline = request.form["deadline"]
    deadline = datetime.datetime.strptime(deadline,'%Y-%m-%d')

    todo = Todo(title=title, deadline=deadline)
    
    db.session.add(todo)
    db.session.commit()
    
    return redirect('/')
    

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)