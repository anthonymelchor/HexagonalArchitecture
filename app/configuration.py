class configuration:
    #This is only an example for this project. Use environment variables or a secure key management solution to store and access your secret key and database info.
    def __init__(self):
        self.db_user = "user"
        self.db_password = "password"
        self.db_host = "mysql-db"
        self.db_name = "ecommerce"
        self.db_uri  = f"mysql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
        self.secret_key = 'your_secret_key'
        self.refresh_key = 'your_refresh_key'
