from flask_login import AnonymousUserMixin


class User(AnonymousUserMixin):
    def __init__(self, uid, email, display_name, is_active, is_admin):
        self.uid = uid
        self.display_name = display_name
        self.email = email
        self.is_active = is_active
        self.is_admin = is_admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.is_active

    def is_admin(self):
        return self.is_admin

    def get_id(self):
        return self.uid

    def __repr__(self):
        return '%r' % self.display_name
