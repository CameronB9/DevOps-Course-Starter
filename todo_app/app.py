import os
from flask import Flask, redirect, render_template, request
from datetime import datetime

from todo_app.view_models.index_view_model import ViewModel
from todo_app.data.db import DB
from todo_app.data.mongo_item import MongoItem

from todo_app.flask_config import Config
from todo_app.kv_secrets import get_secrets


def create_app():
    
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(Config())

    if os.environ["FLASK_ENV"] == "production":
        get_secrets()

    @app.route('/')
    def index():
        db = DB()
        items = db.get_items()
        item_view_model = ViewModel(items)

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
                'modified_date': datetime.now().isoformat(),
                'is_done': False
            }

            if description.strip() != '':
                to_add['description'] = description
            
            if date.strip() != '':
                to_add['due_date'] = datetime.strptime(date, '%d/%m/%Y').isoformat()
            
            db = DB()
            db.add_item(MongoItem.from_dict(to_add, mode = "Save"))
        return redirect('/')

    @app.route('/todo/change-status/<id>', methods=['POST'])
    def change_todo_status(id):
        db = DB()
        item_to_update = db.get_item(id)
        item_to_update.update_status()
        db.update_item(item_to_update)
        return redirect('/')

    @app.route('/todo/delete/<id>', methods=['POST'])
    def delete_todo(id):
        db = DB()
        item_to_delete = db.get_item(id)
        db.delete_item(item_to_delete)
        return redirect('/')
    return app

