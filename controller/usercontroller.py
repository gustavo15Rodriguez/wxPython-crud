from model.model import User
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound
from controller.conection import Conection

class UserController():

    def __init__(self):
        self.conect = Conection()

    def create_user(self, first_name, last_name, username, password):
        user = User(first_name=first_name, last_name=last_name, username=username, password=password)
        session = self.conect.connect_database()
        session.add(user)
        session.commit()
        session.close()

    def get_user(self, id_user):
        session = self.conect.connect_database()

        try:
            user = session.query(User).filter_by(id=id_user).one()
            session.close()
            return user

        except (MultipleResultsFound, NoResultFound):
            return None

    def get_all_users(self):
        session = self.conect.connect_database()
        users = session.query(User).all()
        session.close()
        return users

    def search_user(self, username, password):
        session = self.conect.connect_database()

        try:
            user = session.query(User).filter_by(username=username, password=password).one_or_none()
            session.close()

            if user is not None:
                return True
            return False

        except MultipleResultsFound:
            session.close()
            return False

    def search_username(self, username):
        session = self.conect.connect_database()

        try:
            user = session.query(User).filter_by(username=username).one_or_none()
            session.close()

            if user is not None:
                return user
            return None

        except MultipleResultsFound:
            session.close()
            return False

    def edit_user(self, id_user, data):
        session = self.conect.connect_database()
        user = session.query(User).filter_by(id=id_user).one()
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.username = data['username']
        user.password = data['password']
        session.add(user)
        session.commit()
        session.close()

    def delete_user(self, id_user):
        session = self.conect.connect_database()
        user = session.query(User).filter_by(id=id_user).one()
        session.delete(user)
        session.commit()
        session.close()

    def get_first_name_user(self, first_name):
        session = self.conect.connect_database()

        try:
            user = session.query(User).filter_by(first_name=first_name).one_or_none()
            session.close()
            return user.first_name

        except (MultipleResultsFound, NoResultFound):
            return first_name

    def get_first_name(self, first_name):
        session = self.conect.connect_database()

        try:
            user = session.query(User).filter_by(first_name=first_name).all()
            session.close()
            return user

        except (MultipleResultsFound, NoResultFound):
            return None