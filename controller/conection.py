from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Conection():
    def connect_database(self):
        engine = create_engine("mysql+pymysql://gustavo_admin:12345@localhost/ideas_testing")
        Session = sessionmaker(bind=engine)
        session = Session()
        return session