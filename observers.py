from interface import implements, Interface
from datetime import datetime
import requests


class Observer(Interface):
    def update(self, message: str):
        """
        Update the observer with a new message from the subject.
        """
        pass


class ConsoleLogger(implements(Observer)):
    def update(self, message: str):
        print(f"{message}")


class FileLogger(implements(Observer)):
    def __init__(self, file_name: str):
        self.file_name = file_name

    def update(self, message: str):
        with open(self.file_name, "a") as f:
            f.write(f"{message}\n")


class TelegramLogger(implements(Observer)):
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def update(self, message: str):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": message}
        requests.post(url, data=data)
