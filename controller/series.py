from controller.conection import Conection
from model.model import Serie
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound

class Series():
    def __init__(self):
        self.conect = Conection()

    def create_serie(self, titulo_serie, creador, genero, no_temporadas, estado, imagen_url):
        serie = Serie(titulo_serie=titulo_serie, creador=creador, genero=genero, no_temporadas=no_temporadas, estado=estado, imagen_url=imagen_url)
        session = self.conect.connect_database()
        session.add(serie)
        session.commit()
        session.close()

    def edit_state(self, id_serie, data):
        session = self.conect.connect_database()
        serie = session.query(Serie).filter_by(id=id_serie).one()
        serie.estado = data['estado']
        session.add(serie)
        session.commit()
        session.close()

    def edit_series(self, id_serie, data):
        session = self.conect.connect_database()
        serie = session.query(Serie).filter_by(id=id_serie).one()
        serie.titulo_serie = data['titulo_serie']
        serie.creador = data['creador']
        serie.genero = data['genero']
        serie.no_temporadas = data['no_temporadas']
        serie.estado = data['estado']
        serie.imagen_url = data['imagen_url']
        session.add(serie)
        session.commit()
        session.close()

    def get_serie(self, id_serie):
        session = self.conect.connect_database()

        try:
            serie = session.query(Serie).filter_by(id=id_serie).one()
            session.close()
            return serie

        except (MultipleResultsFound, NoResultFound):
            return None

    def get_all_series(self):
        session = self.conect.connect_database()
        series = session.query(Serie).all()
        session.close()
        return series

    def get_all_images(self):
        session = self.conect.connect_database()

        try:
            serie = session.query(Serie).all()
            list_series = []
            for series in serie:
                list_series.append(series)
            session.close()
            return list_series

        except (MultipleResultsFound, NoResultFound):
            return None

    def get_image(self, text_serie):
        session = self.conect.connect_database()

        try:
            serie = session.query(Serie).filter_by(titulo_serie=text_serie).all()
            print(serie)
            list_serie = []
            for series in serie:
                list_serie.append(series)
            session.close()
            return list_serie

        except (MultipleResultsFound, NoResultFound):
            return None

    def delete_serie(self, id_serie):
        session = self.conect.connect_database()
        serie = session.query(Serie).filter_by(id=id_serie).one()
        session.delete(serie)
        session.commit()
        session.close()

    def get_name_serie(self, titulo_serie):
        session = self.conect.connect_database()

        try:
            serie = session.query(Serie).filter_by(titulo_serie=titulo_serie).all()
            session.close()
            return serie

        except NoResultFound:
            return None











