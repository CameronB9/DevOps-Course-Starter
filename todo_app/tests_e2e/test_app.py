import os
from time import sleep
from threading import Thread
from dotenv import load_dotenv, find_dotenv
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from todo_app import app
from setup import TrelloSetup



@pytest.fixture(scope='module')
def app_with_temp_board():

    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    trello_setup = TrelloSetup()
    board_id = trello_setup.create_board()
    os.environ['TRELLO_BOARD_ID'] = board_id
    todo_list = trello_setup.create_list('To Do', board_id)
    complete_list = trello_setup.create_list('Completed', board_id)
    os.environ['TRELLO_TODO_LIST_ID'] = todo_list
    os.environ['TRELLO_COMPLETED_LIST_ID'] = complete_list


    application = app.create_app()

    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    sleep(1)

    yield application

    thread.join(1)
    trello_setup.delete_board()


@pytest.fixture(scope="module")
def driver():
    with webdriver.Chrome() as driver:
        yield driver

def test_task_journey(driver: WebDriver, app_with_temp_board):
    driver.get('http://localhost:5000')
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





