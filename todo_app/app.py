import os
from flask import Flask, redirect, render_template, request, session
from flask_login import LoginManager, login_required, UserMixin, login_user
from urllib.parse import urlencode
from datetime import datetime
import random
import string
import requests

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


    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():

        state = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        session['state'] = state

        params = {
            'client_id': os.environ['GITHUB_OAUTH_CLIENT_ID'],
            'redirect_uri': f'{os.environ['HOMEPAGE_URL']}/login/callback',
            'state': state,
            'allow_signup': True
        }

        query_str = urlencode(params)

        return redirect(f'{os.environ["GITHUB_OAUTH_URL"]}/authorize?{query_str}')

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    @app.route('/')
    @login_required
    def index():
        db = DB()
        items = db.get_items()
        item_view_model = ViewModel(items)

        return render_template(
            'index.html', 
            view_model = item_view_model
        )

    class User(UserMixin):
        def __init__(self, id) -> None:
            super().__init__()
            self.id = id

    @app.route('/login/callback')
    def login_callback():
        code = request.args.get('code')
        state = request.args.get('state')


        if session['state'] != state:
            return redirect('/login/error')

        params = {
            'client_id': os.environ['GITHUB_OAUTH_CLIENT_ID'],
            'client_secret': os.environ['GITHUB_OAUTH_CLIENT_SECRET'],
            'code': code,
            'redirect_uri': f'{os.environ["HOMEPAGE_URL"]}/login/callback'
        }


        access_response = requests.post(
            f'{os.environ["GITHUB_OAUTH_URL"]}/access_token', 
            json=params,
            headers={
                'Accept': 'application/json'
            }
        ).json()

        token = access_response['access_token']

        user_response = requests.get(
            'https://api.github.com/user',
            headers={
                'Authorization': f'Bearer {token}'
            }
        ).json()

        user_id = user_response['id']

        user = User(user_id)

        login_user(user)

        return redirect('/')

    @app.route('/todo/add', methods=['POST'])
    @login_required
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
    @login_required
    def change_todo_status(id):
        db = DB()
        item_to_update = db.get_item(id)
        item_to_update.update_status()
        db.update_item(item_to_update)
        return redirect('/')

    @app.route('/todo/delete/<id>', methods=['POST'])
    @login_required
    def delete_todo(id):
        db = DB()
        item_to_delete = db.get_item(id)
        db.delete_item(item_to_delete)
        return redirect('/')

    @app.route('/login/error', methods=['GET'])
    def login_error():
        return render_template('login_error.html')            

    return app


