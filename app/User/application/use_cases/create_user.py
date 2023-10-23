from User.domain.entities import User

class CreateUser:
    def __init__(self, user_port):
        self.user_port = user_port
    
    def create_user(self, name, role, email, password, avatar):
        user = User(name, role, email, password, avatar)
        new_user = self.user_port.add(user)
        return new_user