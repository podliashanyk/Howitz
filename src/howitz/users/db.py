import sqlite3

from .model import User


def user_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return User(**{k: v for k,v in zip(fields, row)})


class UserDB:
    class Exception(Exception):
        pass

    def __init__(self, database_file: str):
        connection = sqlite3.connect(database_file)
        connection.row_factory = user_factory
        self.connection = connection
        self.cursor = connection.cursor()

    def initdb(self):
        fields = ', '.join(User.model_fields.keys())
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS user ({fields})")

    def get(self, username):
        querystring = "SELECT * from user where username=?"
        params = (username,)
        query = self.cursor.execute(querystring, params)
        result = query.fetchall()
        if not result:
            return None
        if len(result) > 1:
            raise Exception("More than one with that username, b0rked database")
        return result[0]

    def add(self, user: User):
        querystring = "INSERT INTO user (username, password, token) values (?, ?, ?)"
        params = (user.username, user.password, user.token)
        self.cursor.execute(querystring, params)
        self.connection.commit()
        return self.get(user.username)

    def update(self, user: User):
        querystring = "REPLACE INTO user (username, password, token) values (?, ?, ?)"
        params = (user.username, user.password, user.token)
        self.cursor.execute(querystring, params)
        self.connection.commit()
        return self.get(user.username)

    def remove(self, username):
        querystring = "DELETE from user where username = ?"
        params = (username,)
        self.cursor.execute(querystring, params)
        return self.get(username)
