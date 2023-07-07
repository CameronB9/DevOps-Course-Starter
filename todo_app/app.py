from flask import Flask, redirect, render_template, request
from todo_app.data.trello_items import Trello
from todo_app.utils import get_trello_credentials

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():

    trello = Trello()

    todo_items = trello.get_items()
    num_todos = len(todo_items)
    num_complete_todos = len([item for item in todo_items if item.status == 'Completed'])
    return render_template(
        'index.html', 
        todo_items = todo_items,
        num_todos = num_todos,
        num_complete_todos = num_complete_todos
    )

@app.route('/todo/add', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new-todo-item')
    if new_todo.strip() != '':
        trello = Trello()
        trello.add_item(new_todo)
    return redirect('/')

@app.route('/todo/change-status/<id>', methods=['POST'])
def change_todo_status(id):
    credentials = get_trello_credentials()
    trello = Trello()
    todo_item = trello.get_item(id)
    current_list = todo_item['idList']

    new_list = None

    if current_list == credentials['todo_list']:
        new_list = credentials['completed_list']
    else:
        new_list = credentials['todo_list']

    to_update = {
        'idList': new_list
    }
    trello.update_item(id, to_update)
    return redirect('/')

@app.route('/todo/delete/<id>', methods=['POST'])
def delete_todo(id):
    trello = Trello()
    trello.delete_item(id)
    return redirect('/')