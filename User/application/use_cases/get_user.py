class GetUSer:
    def __init__(self, user_port):
        self.user_port = user_port
    
    def get_user(self, id):
        user = self.user_port.get_user(id)
        return user