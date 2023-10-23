from User.domain.entities import User

class GetUsers:
    def __init__(self, user_port):
        self.user_port = user_port
    
    def get_users(self):
        users = self.user_port.get_users()
        return users
        #return {'message':'User created succesfully'}