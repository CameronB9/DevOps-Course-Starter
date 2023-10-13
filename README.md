# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

The `.env` file also stores Trello credentials which are required to run the app. You will need a [Trello account](https://trello.com/signup) and API key. You can find instructions on how to do this [here](https://trello.com/app-key). Replace the following environment variables in your `.env` file:

```bash
TRELLO_API_KEY=trello-api-key
TRELLO_SECRET=trello-secret
```

After creating a Trello account, you also need to create a board which will be used to store the to do items. This can be done after signing into Trello. Once you've created a board, you can follow the instructions [here](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#your-first-api-call) to find the ID of the board you wish to use. Populate the following environment variable with your board ID:

```bash
TRELLO_BOARD_ID=trello-board-id
```

Once you have created a board, create 2 different lists within the board. One called `To Do` and the other called `Completed`. Get the id of each list using the call below (this can be done with Postman):

```
https://api.trello.com/1/boards/[your-board-id]/lists?key=[your-api-key]&token=[your-api-token]
```

Update the `.env` file with the id of each list

```bash
TRELLO_TODO_LIST_ID=trello-todo-list-id
TRELLO_COMPLETED_LIST_ID=trello-completed-list-id
```



## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Testing

### Running Tests

The app uses the `pytest` testing framework, it's listed as a dependency and will be installed when running `poetry install`. To run the tests, run the following command from the root folder:

```bash
pytest
```

You can run tests in a specific directory by passing the directory as an argument:

```bash
pytest testing/
```

You can also run tests in a specific file:

```bash
pytest todo_app/view_models/test_index_view_model.py
```

### Adding additional tests

You can add more tests by creating an new file with the name test_*.py. Tests should also be prefixed test_*. For more on the test discovery rules, check out [the pytest docs](https://docs.pytest.org/en/stable/explanation/goodpractices.html#conventions-for-python-test-discovery).


## Deployment with Ansible

Clone the repo to the control node:

```bash
git clone git@github.com:CameronB9/DevOps-Course-Starter.git
```

### Creating A Encrypted Vault

Create a YAML file called `secrets.yml` to store our environment variables. Before creating the file, be sure to check out the Ansible Docs on [how to secure your editor](https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#steps-to-secure-your-editor) to avoid accidentally exposing sensitive information. Copy the below code into the file and replace the place holders with your secrets:

```yml
secret_key: [your_secret_key]
trello_api_key: [your_api_key]
trello_secret: [your_trello_secret]
trello_board_id: [your_board_id]
trello_todo_list_id: [your_todo_list_id]
trello_completed_list_id: [your_completed_list_id]
~                                                              
```

After saving and closing the file, run the following command to encrypt your secrets:

```bash
ansible-vault encrypt secrets.yml
```

When prompted, enter and then confirm the password for the file. The password will be required when editing and running the playbook, be sure to keep it safe.

### Editing The Encrypted Vault

To edit the vault, run the following command:

```
ansible-vault edit secrets.yml
```

This will open the file in vim and allow you to edit it. After exiting and saving, the file will be encrypted.

### Running The Ansible Playbook

Before running the playbook, check the `inventory.ini` file to ensure you run the playbook on the required servers. To run the playbook, run the following command:

```bash
ansible-playbook playbook.yml -i inventory.ini --ask-vault-pass
```

Enter your vault password when prompted. Ensure that the `--ask-vault-pass` flag is passed otherwise, the playbook will fail.

### Testing deployment
The Todo app should now be running on each of the servers listed within the `[webservers]` group in the `inventory.ini` file. Open the app within a browser:

`http://[server-ip-address]:80`

## Docker

To run the app in Docker, make sure you have [Docker Desktop](https://docs.docker.com/desktop/wsl/) installed and running. 

### Creating a production-ready container image
From the root directory of the repo, run the following command:

```bash
docker-compose -f docker-compose.prod.yml up --build
```
After running for the first time, you can omit build to skip the build stage.

### Running the development environment
The development environment runs the application and tests. The tests will run every time a file change is detected. The Flask server will also restart when changes are detected.

```bash
docker-compose -f docker-compose.dev.yml up --build
```

by default, the development environment will run flask in debug mode, tests and e2e tests. You can chose specific services by passing additional arguments to the up command. For example, if you only want to run flask, run the below command:

```bash
docker-compose -f docker-compose.dev.yml up dev
```

To run flask and tests run the below command:

```bash
docker-compose -f docker-compose.dev.yml up dev test
```

### Debug code running in container
For this you will need to install the following VSCode Extensions:

- VSCode Docker Extension
- VSCode Remote Development

The following command will run a special debug image:

```bash
docker-compose -f docker-compose.debug.yml up --build
```

The command will start the container but will not run Flask. To run the app in debug mode, follow these steps:

1. Run the compose command outlined above
2. Click on the Docker tab in VSCode
3. Find the `todo-app:debug` container under containers (it will have a green play button next to it)
4. Right click the correct container and select attach VSCode
5. A new VSCode window will open. Click the `Run and Debug` tab
6. Click the `Run and Debug` button
7. Select Flask from dropdown menu that appears
8. Type `todo_app/app.py` into the input box that appears

 