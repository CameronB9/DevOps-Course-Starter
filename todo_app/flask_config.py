import os


class Config:
    def __init__(self):
        """Base configuration variables."""
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        self.LOGIN_DISABLED = os.environ.get('LOGIN_DISABLED') == 'True'
        self.LOG_LEVEL = os.environ.get('LOG_LEVEL')
        self.LOGGLY_TOKEN = os.environ.get('LOGGLY_TOKEN')
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
