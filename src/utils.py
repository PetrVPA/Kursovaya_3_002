import psycopg2
import os.path
from dotenv import load_dotenv
from src.work import APIState
from src.work import APIAirplane

load_dotenv('.env')
word = os.getenv('PASSWORD')

conn = psycopg2.connect(host = "localhost", database = "airplanes_country", port = 5432, user = "postgres",
                        password = word,)

def filter_state(air_boards: list[object], name_state: str) -> list:
    '''
    Функция фильтрации самолетов по стране регистрации
    :param air_boards: список объектов Airplane
    :param name_state: выбранная пользователем страна регистрации для фильтрации
    :return: список бортов зарегистрированных в стране выбранной пользователем
    '''
    state_key = name_state
    plane_state = (x for x in air_boards if x.state == state_key)
    return list(plane_state)


countries = [
    "Germany",
    "France",
    "Poland",
    "Norway"
]


def creat_tables():
    cur = conn.cursor()
    cur.execute("""SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'countries')""")
    kontr_st = cur.fetchone()[0]
    # print(F"{kontr_st} таблица создана")
    if not kontr_st:
        cur.execute("""CREATE TABLE countries (title VARCHAR(50) PRIMARY KEY)""")
    cur.execute("""SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'planes')""")
    kontr_air = cur.fetchone()[0]
    if not kontr_air:
        cur.execute("""CREATE TABLE planes (
                id SERIAL PRIMARY KEY,
                callout VARCHAR(50) NOT NULL,
                velocity FLOAT NOT NULL,                
                true_track FLOAT NOT NULL,
                country_title VARCHAR(50),
                CONSTRAINT FK_CounryPlane
                FOREIGN KEY (country_title) REFERENCES countries(title)

            );""")
    conn.commit()


def save_country_data_to_db(country: str):
    cur = conn.cursor()
    cur.execute("""SELECT * FROM countries WHERE title = %s""", (country,))
    stend = cur.fetchmany()
    any = len(stend)
    if any == 0:
        cur.execute("""INSERT INTO countries (title) VALUES (%s)""", (country,))
    conn.commit()


def save_planes_data_to_db(country: str, plane_data: list):
    callout = plane_data[1]
    if callout is not None:
        velocity = plane_data[9]
        if velocity is not None:
            true_track = plane_data[10]
            if true_track is not None:
                country_title = country
                cur = conn.cursor()
                cur.execute(
                    """INSERT INTO planes (callout, velocity, true_track, country_title) VALUES (%s, %s, %s, %s)""",
                    (callout, velocity, true_track, country_title))
    conn.commit()


state = APIState()
airplane = APIAirplane()


def greet_function(countries: list):

    for country in countries:
        bbox = state.get_coordinates(country)
        #print(bbox)
        plane_box = airplane.get_coordinates(bbox)
        planes = plane_box.get('states')
        #print(planes)
        save_country_data_to_db(country)
        for plane in planes:
            save_planes_data_to_db(country, plane)


class DBManager:

    @staticmethod
    def get_countries_and_aeroplanes_count() -> dict:
        '''
        Метод обращается к базе данных получает список присутствующих в БД стран и предоставляет количество воздушных
        судов (идентификатор позывной воздушного судна) в их воздушном пространстве
        :return: возвращается словарь в виде {'страна1':12345,'страна2':6789}
        '''
        list_state = {}
        cur = conn.cursor()
        cur.execute("""CREATE TEMPORARY TABLE tmp_state_plane AS SELECT title, callout FROM countries INNER JOIN planes
        ON title=planes.country_title""")  # создает таблицу страна - позывной
        cur.execute("""SELECT DISTINCT title FROM tmp_state_plane""") # создает т-у уникальных значений т-цы страны
        real_state = cur.fetchall()
        for row in real_state:
            cur.execute("""SELECT SUM(CASE WHEN title = %s THEN 1 ELSE 0 END) 
            AS col FROM tmp_state_plane; """, (row,))
            state_plane = cur.fetchall()[0][0]
            #print(state_plane)
            list_state[row[0]] = state_plane

        cur.execute("DROP TABLE IF EXISTS temp_table;")
        conn.commit()
        return list_state

    @staticmethod
    def get_all_aeroplanes() -> list:
        list_airplane = []
        cur = conn.cursor()
        cur.execute("""SELECT callout FROM public.planes""")
        tmp_airplane = cur.fetchall()
        for airplane in tmp_airplane:
            list_airplane.append(airplane[0])
        conn.commit()
        return list_airplane

    @staticmethod
    def get_avg_speed():
        cur = conn.cursor()
        cur.execute("""SELECT AVG(velocity) FROM public.planes;""")
        avg_speed = cur.fetchall()
        avg_velocity = avg_speed[0][0]
        avg_velocity = round(avg_velocity, 2)
        conn.commit()
        return avg_velocity

    @staticmethod
    def get_aeroplanes_with_higher_speed() -> list:
        list_airplane = []
        cur = conn.cursor()
        cur.execute("""SELECT AVG(velocity) FROM public.planes;""")
        avg_speed = cur.fetchall()
        avg_velocity = avg_speed[0][0]
        avg_velocity = round(avg_velocity, 2)
        cur.execute("""SELECT callout FROM public.planes WHERE velocity > %s;""", (avg_velocity,))
        tmp_airplane = cur.fetchall()
        for airplane in tmp_airplane:
            list_airplane.append(airplane[0])
        conn.commit()
        return list_airplane

    @staticmethod
    def get_aeroplanes_with_keyword(key: str) -> list:
        list_callout = []
        rem = []
        cur = conn.cursor()
        set = '%' + key + '%'
        cur.execute("""SELECT callout FROM public.planes WHERE callout LIKE %s;""", (set,))
        tmp_list = cur.fetchall()
        for callout in tmp_list:
            list_callout.append(callout[0])
        conn.commit()
        if len(list_callout) == 0:
            rem[0] = "Данное сочетание отсутствует"
            return rem
        else:
            return list_callout
