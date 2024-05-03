import os
from flask import Flask, redirect, render_template, request, session
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
from urllib.parse import urlencode
from datetime import datetime
import random
import string
import requests

from todo_app.view_models.index_view_model import ViewModel
from todo_app.view_models.user_view_model import UserViewModel
from todo_app.data.db import DB
from todo_app.data.mongo_item import MongoItem
from todo_app.data.user_management import UserManagement
from todo_app.user import Roles, User

from todo_app.flask_config import Config
from todo_app.kv_secrets import get_secrets

def create_app():
    
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(Config())

    if os.environ["FLASK_ENV"] == "production":
        get_secrets()


    login_manager = LoginManager()

    if app.config.get('LOGIN_DISABLED') == True:
        login_manager.anonymous_user = lambda : User('TEST_USER', Roles.writer)
    
    @login_manager.unauthorized_handler
    def unauthenticated():

        state = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        session['state'] = state

        params = {
            'client_id': os.environ['GITHUB_OAUTH_CLIENT_ID'],
            'redirect_uri': f'{os.environ["HOMEPAGE_URL"]}/login/callback',
            'state': state,
            'allow_signup': True
        }

        query_str = urlencode(params)

        return redirect(f'{os.environ["GITHUB_OAUTH_URL"]}/authorize?{query_str}')


    @login_manager.user_loader
    def load_user(user_id):
        user_management = UserManagement()
        user = user_management.get_user(user_id)
        return user
        #return User(user_id)

    login_manager.init_app(app)

    @app.route('/')
    @login_required
    def index():
        db = DB()
        items = db.get_items()
        error = request.args.get('e')
        user = current_user
        item_view_model = ViewModel(items, error)
        user_view_model = UserViewModel(user)

        return render_template(
            'index.html', 
            view_model = item_view_model,
            user_view_model = user_view_model,
            Roles = Roles
        )


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
        username = user_response['login']
        user_management = UserManagement()
        user = user_management.get_user(user_id)

        if user is None:
            num_users = len(user_management.get_users())
            role = Roles.admin if num_users == 0 else Roles.reader
            user = user_management.add_user(user_id, username, role)

        login_user(user)

        return redirect('/')

    @app.route('/todo/add', methods=['POST'])
    @login_required
    @User.check_permission('write')
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
    @User.check_permission('write')
    def change_todo_status(id):
        db = DB()
        item_to_update = db.get_item(id)
        item_to_update.update_status()
        db.update_item(item_to_update)
        return redirect('/')

    @app.route('/todo/delete/<id>', methods=['POST'])
    @login_required
    @User.check_permission('write')
    def delete_todo(id):
        db = DB()
        item_to_delete = db.get_item(id)
        db.delete_item(item_to_delete)
        return redirect('/')

    @app.route('/login/error', methods=['GET'])
    def login_error():
        return render_template('login_error.html')            

    @app.route('/user/management', methods=['GET'])
    @User.check_permission('admin')
    def user_management():

        user_view_model = UserViewModel(current_user)
        user_management = UserManagement()
        users = user_management.get_users()

        return render_template('user_management.html',
            user_view_model = user_view_model,
            users = users,
            roles = Roles
        )

    @User.check_permission('admin')
    @app.route('/user/management/update/<id>', methods=['POST'])
    def update_user(id):
        role = request.form.get('role')
        user_management = UserManagement()
        if role in Roles.list():
            user_management.update_user_role(id, role)
        return redirect('/user/management')

    return app



