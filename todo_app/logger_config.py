import os
from datetime import datetime
from pythonjsonlogger.jsonlogger import JsonFormatter

class LogCategory:
    login = 'LOGIN'
    setup = 'SETUP'
    todo = 'MANAGE_TODO'
    user = 'USER_MANAGEMENT'

class LogAction:
    add_todo = 'ADD_TODO'
    update_todo = 'UPDATE_TODO'
    delete_todo = 'DELETE_TODO'
    update_role = 'UPDATE_ROLE'
    permission = 'INSUFFICIENT_PERMISSION'


class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

        log_record['FLASK_ENV'] = os.environ.get('FLASK_ENV')