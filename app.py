from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # https://flask.palletsprojects.com/en/2.2.x/tutorial/factory/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # https://flask-sqlalchemy.palletsprojects.com/en/2.x
# /config/
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    complete = db.Column(db.Boolean, nullable=False)


@app.route('/')
def index():  # put application's code here
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=80)

    #https://www.youtube.com/watch?v=Z1RJmh_OqeA&t=1207s
    #https://www.youtube.com/watch?v=yKHJsLUENl0&t=389s
