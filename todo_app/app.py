from flask import Flask, redirect, render_template, request
from datetime import datetime

from todo_app.data.trello_items import Trello
from todo_app.utils import get_trello_credentials
from todo_app.view_models.index_view_model import ViewModel

from todo_app.flask_config import Config


def create_app():
    
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(Config())

    @app.route('/')
    def index():

        trello = Trello()

        todo_items = trello.get_items_sorted()

        item_view_model = ViewModel(todo_items)

        return render_template(
            'index.html', 
            view_model = item_view_model
        )

    @app.route('/todo/add', methods=['POST'])
    def add_todo():
        name = request.form.get('todo-name')
        description = request.form.get('todo-description')
        date = request.form.get('todo-due-date')

        if name.strip() != '':

            to_add = {
                'name': name,
            }

            if description.strip() != '':
                to_add['desc'] = description
            
            if date.strip() != '':
                to_add['due'] = datetime.strptime(date, '%d/%m/%Y').isoformat()
            

            trello = Trello()
            trello.add_item(to_add)
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
   #  hello
    return app
file = __file__
if __name__ == 'todo_app.app':
    create_app()

