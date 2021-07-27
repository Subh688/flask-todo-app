# *****************************FLASK MINIMAL APP****************************

from flask import Flask, render_template, request, redirect # importing Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy # importing SQLAlchemy
from datetime import datetime # importing datetime

app = Flask(__name__) # initializing app
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db" # initialize sqlalchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # signal emitting
db = SQLAlchemy(app) # all set

# defining database schema through a class
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

'''
to generate todo.db
1. Open python interpreter in correct path
2. >>>from app import db
3. >>>db.create_all()
'''

# basic routing and rendering a template
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc) # creating an instance for todo
        db.session.add(todo) # adding the todo to the database
        db.session.commit() # commit the changes
        
    allTodo = Todo.query.all() # fetching all the todos
    return render_template('index.html', allTodo=allTodo) # passing all todos with a variable named allTodo

@app.route('/show')
def show():
    allTodo = Todo.query.all() # fetching all the todos
    print(allTodo) # printing all the todos
    return render_template('index.html', allTodo=allTodo) # passing all todos with a variable named allTodo

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title'] # requesting title of todo
        desc = request.form['desc'] # requesting description of todo
        todo = Todo.query.filter_by(sno=sno).first() # filter todo which we have to update
        todo.title = title # updating title
        todo.desc = desc # updating description
        db.session.add(todo) # add changes
        db.session.commit() # commit the changes
        return redirect("/") # redirecting to home page
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first() # filter todo which we have to delete
    db.session.delete(todo) # deleting the todo
    db.session.commit() # commit the changes
    return redirect("/") # redirecting to home page

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# running app on port 8000
if __name__ == "__main__":
    app.run(debug=True, port=8000)