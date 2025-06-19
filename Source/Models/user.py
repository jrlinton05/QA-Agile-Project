from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username, is_admin=False):
        self.username = username
        self.is_admin = is_admin

    def get_id(self):
        return self.username

    def get_is_admin(self):
        return self.is_admin

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False