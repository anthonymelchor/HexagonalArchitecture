from User.application.ports.user_port import UserPort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from User.domain.user_entity import UserEntity

class UserAdapter(UserPort):
    
    def __init__(self, configuration):
        self.db_uri = configuration.db_uri
        self.engine = create_engine(self.db_uri)
        self.Session = sessionmaker(bind=self.engine)

    def add(self, user):
        try:
            session = self.Session()
            new_user = UserEntity(name = user.name, role = user.role, email = user.email, password = user.password, avatar = user.avatar)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            session.close()
            return new_user
        except Exception as e:
            session.rollback()
            raise e
    
    def get_users(self):
        try:
            session = self.Session()
            users = session.query(UserEntity).all()
            session.close()
            return users
        except Exception as e:
            raise e
        
    def get_user(self, id):
        try:
            session = self.Session()
            user = session.query(UserEntity).filter_by(id=id).first()
            session.close()
            return user
        except Exception as e:
            raise e
        
    def update_user(self, id, payload):
        try:
            with self.Session() as session:
                user = session.query(UserEntity).filter_by(id=id).first()
                
                if user:
                    for key, value in payload.items():
                        setattr(user, key, value)
                    
                    session.commit()
                    session.refresh(user)
                    session.close()
                    
                return user
        except Exception as e:
            session.rollback()
            raise e
    
    def login_user(self, email, password):
        try:
            session = self.Session()
            user = session.query(UserEntity).filter_by(email=email, password=password).first()
            session.close()
            return user
        except Exception as e:
            raise e


    def email_exists(self, email):
        try:
            session = self.Session()
            user = session.query(UserEntity).filter_by(email=email).first()
            session.close()
            if user is not None:
                return True
            else:
                return False
        except Exception as e:
            raise e
        
