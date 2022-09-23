import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, OperationalError
from psycopg2 import errors
UniqueViolation = errors.lookup('23505')

from db_functions.functions_db_ORM import Check_grenhouse, Check_tray
import json

from logger_funcs.color_logger import out_red, out_violet

user = "postgres"
password = "02468"
host = "141.144.192.157"
# host = "localhost"
database = "greenhouse_db"
path_root = 'abc'
path = 'oracl/primaty/'
path_sort_photo = 'oracle/sort_photo'
path_process = 'oracl/for_home/'
sms = 'list,of,photo'
global last_photo_loaded, last_photo_processed, id_photo, id_accident, list_deasise
diseases = {'bad': 0, 'fall': 1, 'good': 2, 'smallbad': 3, 'undefined': 4}
global id_photo, id_accident
id_photo = 0
id_accident = 0



# Base = declarative_base(bind=engine)
# metadata = MetaData(bind=engine)

def add_photo_and_acc(input_data, server_photo_lib_path, dbArgs):
    engine = dbArgs["engine"]
    Photo = dbArgs["Photo"]
    Accident = dbArgs["Accident"]
    global path
    path = server_photo_lib_path
    json_data = json.loads(input_data)
    name_photo = json_data['img_name'].split('.')[0]
    path_photo = path + json_data['img_name']
    fk_id_tray = Check_tray()
    fk_id_greenhouse = Check_grenhouse()
    Session = sessionmaker(bind=engine)
    createSession_flag = False
    while not createSession_flag:
        try:
            session = Session()
            createSession_flag = True
        except Exception as e:
            out_red("Error with creating new Session")
            out_red(e)
    print("Database opened successfully")

    photo = Photo(name_photo=name_photo,
                  path_photo=path_photo,
                  loaded=True, processed=True,
                  fk_id_tray=fk_id_tray,
                  fk_id_greenhouse=fk_id_greenhouse)
    addPhoto_flag = False
    while not addPhoto_flag:
        try:
            session.add(photo)
            session.commit()
            addPhoto_flag = True
            print("Record inserted successfully")
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                out_red("This photo already in DB")
                addPhoto_flag = True
                session.rollback()
        except OperationalError as e:
            if isinstance(e.orig, psycopg2.OperationalError):
                out_red(e)
                session.rollback()
    id_num_photo = session.query(Photo).filter(Photo.name_photo == '{0}'.format(name_photo)).first().id_photo

    for accident in json_data['data']:
        coordinates = accident['coordinates']
        probability = accident['accuracy']
        fk_id_greenhouse = fk_id_greenhouse
        fk_id_tray = fk_id_tray
        fk_id_disease = diseases[accident['disease']]
        fk_id_photo = id_num_photo
        accident = Accident(
            coordinates=coordinates,
            probability=probability,
            fk_id_greenhouse=fk_id_greenhouse,
            fk_id_tray=fk_id_tray,
            fk_id_disease=fk_id_disease,
            fk_id_photo=fk_id_photo)
        addAccident_flag = False
        while not addAccident_flag:
            try:
                session.add(accident)
                session.commit()
                print("Record inserted successfully")
                addAccident_flag = True
            except IntegrityError as e:
                if isinstance(e.orig, UniqueViolation):
                    out_red("This accident already in DB")
                    addAccident_flag = True
                    session.rollback()

    session.close()

# test data
# input_data = '{"img_name": "2279.JPG", "data": ' \
#     '[{"disease":"mite","accuracy":82.32, "coordinates": "599,322;737,460"},' \
#     ' {"disease":"mite","accuracy": 68.46, "coordinates": "46,322;184,506"}]}'