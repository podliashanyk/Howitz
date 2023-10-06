from howitz import database


__all__ = [
    "authenticate_user",
]


def authenticate_user(username, password):
    user = database.get(username)
    if user and user.authenticate(password):
        return user
    return None
