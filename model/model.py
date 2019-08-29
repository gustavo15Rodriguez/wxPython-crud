from sqlalchemy import Column, create_engine
from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://gustavo_admin:12345@localhost/ideas_testing")
DeclarativeBase = declarative_base(engine)
metadata = DeclarativeBase.metadata

class User(DeclarativeBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column("first_name", String(20))
    last_name = Column("last_name", String(20))
    username = Column("username", String(20), unique=True)
    password = Column("password", String(20))

    def __repr__(self):
        return "<username: %s>"%(self.username)

class Videojuego(DeclarativeBase):
    __tablename__ = "videojuegos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo_videojuego = Column("titulo videojuego", String(30), unique=True)
    compania = Column("compañia", String(20))
    genero = Column("genero", String(15))
    horas_duracion = Column("horas duracion", String(5))
    estado = Column("estado", String(20))
    imagen_url = Column("Url Imagen", String(200))

    def __repr__(self):
        return "<Videojuego, compañia, genero, horas duracion, estado, imagen_url: %s %s %s %s %s %s>"%(self.titulo_videojuego, self.compania, self.genero, self. horas_duracion, self.estado, self.imagen_url)

class Serie(DeclarativeBase):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo_serie = Column("titulo serie", String(50), unique=True)
    creador = Column("creador", String(20))
    genero = Column("genero", String(15))
    no_temporadas = Column("numero temporadas", Integer)
    estado = Column("estado", String(10))
    imagen_url = Column("Url Imagen", String(200))

    def __repr__(self):
        return "<Serie, creador, genero, No. temporadas, estado, imagen_url: %s %s %s %s %s %s>" % (self.titulo_serie, self.creador, self. genero, self.no_temporadas, self.estado, self.imagen_url)

class Rentas(DeclarativeBase):
    __tablename__ = "rentas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("usuario", Integer)
    id_renta = Column("tipo de renta", Integer)
    estado_renta = Column("estado", String(10))

    def __repr__(self):
        return "<Clave de Usuario: %d>" % (self.id_usuario)

metadata.create_all()