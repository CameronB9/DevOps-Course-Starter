from functools import wraps
import os
from time import sleep
from threading import Thread
from dotenv import load_dotenv, find_dotenv

import pymongo
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from todo_app import app

db_name = 'E2E_TEST_todo-db'
port = "5867"

def delete_db():
    client = pymongo.MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
    client.drop_database(db_name)

@pytest.fixture(scope="module")
def app_with_temp_db():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    os.environ['MONGO_DATABASE_NAME'] = db_name
    os.environ['LOGIN_DISABLED'] = "True"


    if os.environ["E2E_CREATE_TEMP_APP"] == "True":
        application = app.create_app()

        thread = Thread(target=lambda: application.run(use_reloader=False, port=port))
        thread.daemon = True
        thread.start()
        sleep(1)

        yield application

        thread.join(1)
        delete_db()


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=options) as driver:
        yield driver

def test_task_journey(driver: WebDriver, app_with_temp_db):
    
    url = os.environ["E2E_TEST_URL"]

    driver.get(url)
    assert driver.title == 'To-Do App'

    input = driver.find_element(By.ID, 'todo-name')
    todo_name = 'Test Item 1'
    input.send_keys(todo_name)

    submit_btn = driver.find_element(By.ID, "add-todo")
    submit_btn.click()

    assert "Test Item 1" in driver.page_source

    complete_btn_title = f"Mark {todo_name} as Completed"
    complete_btn = driver.find_element(By.XPATH, f"//*[@title='{complete_btn_title}']")
    complete_btn.click()

    assert 'Everything is complete, you can relax for now!' in driver.page_source


    todo_btn_title = f"Mark {todo_name} as To Do"
    todo_btn = driver.find_element(By.XPATH, f"//*[@title='{todo_btn_title}']")
    todo_btn.click()

    assert "What are you waiting for, there's 1 left!" in driver.page_source
