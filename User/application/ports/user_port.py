from abc import ABC, abstractmethod

class UserPort(ABC):
    
    @abstractmethod
    def add(self, user):
        pass

    @abstractmethod   
    def get_users(self):
        pass

    @abstractmethod
    def email_exists(self, email):
        pass    

    @abstractmethod
    def login_user(self, email, password):
        pass
    
    @abstractmethod
    def get_user(self, id):
        pass
