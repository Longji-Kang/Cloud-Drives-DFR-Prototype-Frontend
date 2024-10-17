import sqlite3
import hashlib

class DB_Interface:
    def __connect(self):
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row

        return connection

    def login(self, username: str, password: str) -> bool:
        connection = self.__connect()

        user = connection.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()

        print(username)

        if user is None:
            return False
        else:
            salt = user['salt']
            salt_pass = f'{salt}{password}'

            hash = hashlib.sha256(salt_pass.encode('utf-8')).hexdigest()

            try:
                if hash == user['pass']:
                    return True
                else:
                    return False
            finally:
                connection.close()