from User.domain.entities import User


class UpdateUser:

    def __init__(self, user_adapter):
        self.user_adapter = user_adapter
    
    def update_user(self, id, payload):
        user = self.user_adapter.get_user(id)
        if user:
            user_updated = self.user_adapter.update_user(id, payload)
            return user_updated
        else:
            return None