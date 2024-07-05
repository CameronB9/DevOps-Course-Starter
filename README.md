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

The `.env` file also stores Mongo DB credentials which are required to run the app. It is recommended to use the Mongo DB Comos DB in Azure. You can find instructions on how to do this [here](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/quickstart-dotnet?tabs=azure-cli&pivots=devcontainer-codespace). Replace the following environment variables in your `.env` file:

```bash
MONGO_CONNECTION_STRING=[mongo-connection-string]
MONGO_DATABASE_NAME=[db-name]
TRELLO_API_KEY=[trello-api-key]
TRELLO_SECRET=[trello-secret]
TRELLO_BOARD_ID=[trello-board-id]
```

Although this application no longer uses Trello for data storage, to use the migration script, the `TRELLO_` variables will need to be set.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

The app should be running on port 5000. You should see output similar to the following:
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

## Authentication

The app uses GitHub authentication using the "authorization code" OAuth flow. Users will be redirected to GitHub to sign in before they can access the site. Users and their roles are stored in the database There are 3 different user roles:

| Role               | Description                                                   |
| ------------------ | ------------------------------------------------------------- |
| Admin              | Can read, add, update and delete todos. Can change user roles |
| Writer             | Can read, add, update and delete todos.                       |
| Reader             | read only                                                     |

The first user is given the admin role subsequent users get the reader role. Admin users can manage roles for all users using the `/user/management page`

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
The development environment runs the application and tests. The tests will run every time a file change is detected. The Flask server will also restart when changes are detected. It will also run the dev database which runs in a separate container.

It is recommended to create another .env file for running the development environment. This allows a dev database to be used. Create a new .env file called `.env.docker.dev`:

```bash
FLASK_APP=todo_app/app
FLASK_RUN_HOST=0.0.0.0
FLASK_ENV=docker
FLASK_RUN_PORT=5000

SECRET_KEY=secret-key

KEY_VAULT_NAME=todo-app

MONGO_CONNECTION_STRING=mongodb://[dev-db-username]:[dev-db-password]@[mongo-container-name]:27017/
MONGO_DATABASE_NAME="todo-db"
MONGO_INITDB_ROOT_USERNAME=[dev-db-username]
MONGO_INITDB_ROOT_PASSWORD=[dev-db-password]
```

The variables can all be the same aside from the one prefixed with `MONGO_`. The connection string is made up of the username, password and container name. The container name is set within the `docker-compose.dev.yml` file:

```yml
  mongo-db:
    image: mongo:7.0
    container_name: mongo_container
    restart: always
    ports:
      - 27017:27017
    env_file:
      - .env.docker.dev
    volumes:
      - ./dev_db:/data/db
```

For example, if the username is `admin`, password is `abcdefg` and container name is `mongo_container`, the connection string would be:

```bash
mongodb://admin:abcdefg@mongo_container:27017/
```

Use the following command to run the dev container:

```bash
docker-compose -f docker-compose.dev.yml up --build
```

by default, the development environment will run flask in debug mode, tests and e2e tests. The app should run on port 5000. You can chose specific services by passing additional arguments to the up command. For example, if you only want to run flask, run the below command:

```bash
docker-compose -f docker-compose.dev.yml up dev
```

To run flask and tests run the below command:

```bash
docker-compose -f docker-compose.dev.yml up dev test
```

#### Development Database



### Running tests in a container

Unit and integration tests can be ran using the below command:

```bash
docker-compose -f docker-compose.test-ci.yml run test-ci
```

The docker-compose file was designed with CI in mind. The `.env` file is not available in the CI environment, the e2e tests need the real secrets to work properly. For the e2e tests to work, you need to supply the secrets from the `.env file` using the -e flag. Here's how it is used in the github action workflow:

```bash
docker-compose -f docker-compose.test-ci.yml run \
-e SECRET_KEY=${{ secrets.SECRET_KEY }} \
-e MONGO_CONNECTION_STRING="${{ secrets.MONGO_CONNECTION_STRING }}" \
-e MONGO_DATABASE_NAME=${{ secrets.MONGO_DATABASE_NAME }} \
e2e-ci
```

Each secret is stored as a variable in the repo to avoid making the secrets public.


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

## Deployment to Azure (Manually) 

The application is deployed through Azure App Service using Docker. New changes will need to be pushed to Docker Hub.
The URL is : [https://cb-todo-app.azurewebsites.net/](https://cb-todo-app.azurewebsites.net/).
### Pushing image to Docker Hub
The existing repo can be found on [Docker Hub](https://hub.docker.com/layers/cameronb9/todo-app/prod/images/sha256-0af45a7f075cdb5563052c378e19e048ae5fe3d620168dce73ca7b66818d4ac8?context=repo). First make sure you are logged into DockerHub locally:

```bash
docker login
```

 After making changes to the application, build a new production Docker image using `docker-compose` from the project root directory:

```bash
docker-compose -f docker-compose.prod.yml build
```

This will create a new image with the image tag `todo-app:prod`. The updated image then needs to be pushed to DockerHub:

```
docker push cameronb9/todo-app:prod
```

### Updating the App Service Container

The container can be updated by making a post request to the webhook URL. This will cause the app to restart and pull the latest version of the given container from DockerHub. The webhook URL can be found via the Azure Portal. Go to the app service page and then click on the `Deployment Center` tab. Enter the below command into a terminal to update the app:

```bash
curl -dH -X POST "https://\$<deployment_username>:<deployment_password>@<webapp_name>.scm.azurewebsites.net/docker/hook" 
```

The dollar sign will need to be escaped using a backslash: `\$`. The response to the curl command will contain a link to a log-stream.

## Terraform
The Azure resources are managed by terraform. The configuration can be found in the `terraform/modules` directory. There are 2 different configurations which use the base module. The base module accepts a variable parameter `prefix` which gets appended to the start of the resource name:

```
// app service created by the prod configuration
prod-cb-todo-app-sp-tf
// app service created by the test configuration
test-cb-todo-app-sp-tf
```

The prod configuration is used for the production app. It contains it's own configuration for the database storage account with destroy protection enabled to avoid the production database being deleted. 
Production deployment is automated in the CI Pipeline, to run it manually:

```bash
cd terraform/modules/prod && terraform apply
```

The test configuration is mainly used within the CI pipeline to create a test environment that E2E 
tests are run against, it then gets destroyed. It also has a separate db account that has destroy
 protection enabled. to run it manually, run the following command:

 ```bash
 cd terraform/modules/test && terraform apply
 ```
 
 Both can be destroyed by running the following command:

 ```bash
cd terraform/modules/<module> && terraform destroy
 ```

The terraform state is stored in an azure storage account. There is separate state for test and 
prod configurations. 


## Deployment to Azure (CI Pipeline)
The CI Pipeline automatically publishes the application to Azure. This only happens when the target branch is main and the event type is push (this occurs after a pull request is merged or direct push which is not recommend).  

The CI pipeline runs also a terraform apply to automatically update any changes in the terraform config.

## Migrating Trello Data to Mongo DB

A script has been setup to copy data from trello to mongo DB. In order for the script to work, the `TRELLO_` variables need to be set in the `.env` file. To run the script run the following command from the root directory of this project:

```bash
python scripts/migrate_trello_to_mongo.py
```

## Application Logging
HTTP and custom application logs are stored in [Loggly](https://documentation.solarwinds.com/en/success_center/loggly/content/admin/python-http.htm?cshid=loggly_python-http). By default only production logs get send to Loggly. To capture logs from running the app through docker locally, sign up for a Loggly account and [Generate a token](https://documentation.solarwinds.com/en/success_center/loggly/content/admin/customer-token-authentication-token.htm). Add the token in the `docker.env.dev` file:

```bash
LOGGLY_TOKEN=[loggly-token-here]
```

To correctly configure the production logs, create a secret in GitHub Actions called `TF_VAR_LOGGLY_TOKEN` which contains the Loggly token. The token gets passed into Terraform and is set as an environment variable in the app service settings.
