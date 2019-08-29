from model.model import Videojuego
from controller.conection import Conection
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound

class VideoGame():

    def __init__(self, *args):
        self.conect = Conection()

    def create_game(self, titulo_videojuego, compania, genero, horas_duracion, estado, imagen_url):
        game = Videojuego(titulo_videojuego=titulo_videojuego, compania=compania, genero=genero, horas_duracion=horas_duracion, estado=estado, imagen_url=imagen_url)
        session = self.conect.connect_database()
        session.add(game)
        session.commit()
        session.close()
    def edit_state(self, id_game, data):
        session = self.conect.connect_database()
        game = session.query(Videojuego).filter_by(id=id_game).one()
        game.estado = data['estado']
        session.add(game)
        session.commit()
        session.close()

    def edit_game(self, id_game, data):
        session = self.conect.connect_database()
        game = session.query(Videojuego).filter_by(id=id_game).one()
        game.titulo_videojuego = data['titulo_videojuego']
        game.compania = data['compania']
        game.genero = data['genero']
        game.horas_duracion = data['horas_duracion']
        game.estado = data['estado']
        game.imagen_url = data['imagen_url']
        session.add(game)
        session.commit()
        session.close()

    def get_game(self, id_game):
        session = self.conect.connect_database()

        try:
            game = session.query(Videojuego).filter_by(id=id_game).one()
            session.close()
            return game

        except (MultipleResultsFound, NoResultFound):
            return None

    def get_all_games(self):
        session = self.conect.connect_database()
        games = session.query(Videojuego).all()
        session.close()
        return games

    def get_all_images_games(self):
        session = self.conect.connect_database()

        try:
            game = session.query(Videojuego).all()
            list_games = []
            for games in game:
                list_games.append(games)
            session.close()
            return list_games

        except (MultipleResultsFound, NoResultFound):
            return None

    def delete_game(self, id_game):
        session = self.conect.connect_database()
        game = session.query(Videojuego).filter_by(id=id_game).one()
        session.delete(game)
        session.commit()
        session.close()
