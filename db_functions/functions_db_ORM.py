import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, String, Float, Boolean, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from logger_funcs.color_logger import out_green

user="*********"
password = "*********"
host="*********"
database="*********"
path_root='*********'
path='oracl/primaty/'
path_sort_photo='oracle/sort_photo'
path_process='oracl/for_home/'
sms='list,of,photo'
global last_photo_loaded,last_photo_processed,id_photo,id_accident,list_deasise
last_photo_loaded='0'
last_photo_processed='0'
id_photo=0
id_accident=0



def init_db_tables():
    engine = create_engine("postgresql+psycopg2://postgres:*********@{0}/greenhouse_db".format(host), echo=True)
    print("Getting GB Structure...")
    Base = declarative_base(bind=engine)
    metadata = MetaData(bind=engine)

    class Disease(Base):
        """"""
        __table__ = Table('disease', metadata, autoload=True)
        __tablename__ = 'disease'
        __table_args__ = {'autoload': True}


    class Greenhouse(Base):
        """"""
        __table__ = Table('greenhouse', metadata, autoload=True)
        __tablename__ = 'greenhouse'
        __table_args__ = {'autoload': True}


    class Photo(Base):
        """"""
        __table__ = Table('photo', metadata, autoload=True)
        __tablename__ = 'photo'
        __table_args__ = {'autoload': True}


    class Tray(Base):
        """"""
        __table__ = Table('tray', metadata, autoload=True)
        __tablename__ = 'tray'
        __table_args__ = {'autoload': True}


    class Accident(Base):
        """"""
        __table__ = Table('accident', metadata, autoload=True)
        __tablename__ = 'accident'
        __table_args__ = {'autoload': True}
    out_green("ORM structure got!")

    return {"engine": engine, "Photo": Photo, "Accident": Accident}

# Base.metadata.create_all(engine)

def Check_grenhouse():
    return 1


def Check_tray():
    return 1

