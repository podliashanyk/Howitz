from flask_login import UserMixin
from pydantic import BaseModel


class User(UserMixin, BaseModel):
    username: str
    password: str
    token: str

    def get_id(self):
        return self.username

    @staticmethod
    def encode_password(password):
        # needs much magic!
        return password

    def check_password(self, password):
        return self.password == self.encode_password(password)

    def authenticate(self, password):
        if self.check_password(password):
            return True
        return False
