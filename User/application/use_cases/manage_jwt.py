import jwt
import datetime

class CreateJWT:
    
    def __init__(self, configuration):
        self.secret_key = configuration.secret_key
        self.refresh_key = configuration.refresh_key

    def create_token(self, user):
        try:
            accees_token = jwt.encode({'user': user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1200)}, self.secret_key, algorithm='HS256')
            refresh_token = jwt.encode({'user': user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=2400)}, self.refresh_key, algorithm='HS256')
            return accees_token, refresh_token
        except Exception as e:
            raise e

    def validate_access_token(self, token):
        try:
            user_info = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return user_info
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception as e:
            raise e
        
    def validate_refresh_token(self, token):
        try:
            user_info = jwt.decode(token, self.refresh_key, algorithms=["HS256"])
            return user_info
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None    
        except Exception as e:
            raise e

    def renew_access_token(self, refresh_token):
        try:
            user_info = self.validate_refresh_token(refresh_token)
            if user_info:
                return self.create_token(user_info)[0]
            else:
                return None
        except Exception as e:
            raise e

    def get_user_profile(self, token):
        try:
            profile = jwt.decode(token, self.secret_key,algorithms=["HS256"])
            return profile
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None 
        except Exception as e:
            raise e


