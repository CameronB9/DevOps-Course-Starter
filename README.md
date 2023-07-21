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
