from flask import Flask, redirect, render_template, request
from todo_app.data.session_items import get_items, add_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    todo_items = get_items()
    return render_template('index.html', todo_items = todo_items)

@app.route('/add-todo', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new-todo-item')
    add_item(new_todo)
    return redirect('/')