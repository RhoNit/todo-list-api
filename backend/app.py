from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    status = db.Column(db.Boolean)


# API section
# root API to list all the created todo resources
@app.route('/')
def root():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)


# API/Route to create a todo resource
@app.route('/create', methods=['POST'])
def create_todo():
    todo_title = request.form.get("title")
    new_todo = Todo(title=todo_title, status=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("root"))


# API to mark complete/not complete status of a todo resource (by id)
@app.route('/mark/<int:todo_id>')
def mark_completion(todo_id):
    todo_obj = Todo.query.filter_by(id=todo_id).first()
    todo_obj.status = not todo_obj.status
    db.session.commit()
    return redirect(url_for("root"))


# API to delete a todo resource (by id)
@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    todo_obj = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo_obj)
    db.session.commit()
    return redirect(url_for("root"))


if __name__ == "__main__":
    app.run(debug=True)
