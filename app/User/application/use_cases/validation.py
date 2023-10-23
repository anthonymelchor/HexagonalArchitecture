class Validation:
    def __init__(self, user_port):
        self.user_port = user_port

    def email_exists(self, email):
        email_exists = self.user_port.email_exists(email)
        return email_exists

