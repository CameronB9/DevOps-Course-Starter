from flask import Flask, redirect, render_template, request
from todo_app.data.session_items import get_items, get_item, add_item, save_item, delete_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    todo_items = get_items()
    num_todos = len(todo_items)
    num_complete_todos = len([item for item in todo_items if item['status'] == 'Completed'])
    sorted_items = sorted(todo_items, key = lambda item: item['status'], reverse=True)
    return render_template(
        'index.html', 
        todo_items = sorted_items,
        num_todos = num_todos,
        num_complete_todos = num_complete_todos
    )

@app.route('/todo/add', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new-todo-item')
    if new_todo.strip() != '':
        add_item(new_todo)
    return redirect('/')

@app.route('/todo/change-status/<id>', methods=['POST'])
def change_todo_status(id):
    todo_item = get_item(id)
    current_status = todo_item['status']
    new_status = 'Completed' if current_status == 'Not Started' else 'Not Started'
    todo_item['status'] = new_status

    save_item(todo_item)

    return redirect('/')

@app.route('/todo/delete/<id>', methods=['POST'])
def delete_todo(id):
    todo_item = get_item(id)
    delete_item(todo_item)

    return redirect('/')