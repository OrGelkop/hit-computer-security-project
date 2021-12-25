class User():
    def __init__(self, uid, email, is_active):
        self.uid = uid
        self.username = email
        self.email = email
        self.is_active = is_active

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.is_active

#    def is_anonymous(self):
#        return False

    def get_id(self):
        return self.uid

    def __repr__(self):
        return '%r' % self.username
