from db_interface import DB_Interface

class LoginHandler:
    def __init__(self):
        self.db = DB_Interface()

    def login(self, username: str, password: str):
        return self.db.login(username, password)