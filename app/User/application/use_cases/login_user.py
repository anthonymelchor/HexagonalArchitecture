class LoginUser:

    def __init__(self, user_port):
        self.user_port = user_port
    
    def login_user(self, email, password):
        user = self.user_port.login_user(email, password)
        return user