import psycopg2
import os.path
from dotenv import load_dotenv

load_dotenv('../.env')
word = os.getenv('PASSWORD')

conn = psycopg2.connect(
    host = "localhost",
    database = "airplanes_country",
    port = 5432,
    user = "postgres",
    password = word,
)


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

class DBManager():

    def get_all_aeroplanes() -> dict:
        '''
        Метод обращается к базе данных получает список присутствующих в БД стран и предоставляет количество воздушных
        судов (идентификатор позывной воздушного судна) в их воздушном пространстве
        :return: возвращается словарь в виде {'страна1':12345,'страна2':6789}
        '''
        list_state = {}
        cur = conn.cursor()
        cur.execute(
            """CREATE TEMPORARY TABLE tmp_state_plane AS SELECT title, callout FROM countries INNER JOIN planes ON title=planes.country_title""")  # создает таблицу страна - позывной
        cur.execute(
            """SELECT DISTINCT title FROM tmp_state_plane""")  # создает таблицу уникальных значений таблицы страны
        real_state = cur.fetchall()
        for row in real_state:
            cur.execute("""SELECT SUM(CASE WHEN title = %s THEN 1 ELSE 0 END) AS col FROM tmp_state_plane; """, (row,))
            state_plane = cur.fetchall()[0][0]
            print(state_plane)
            list_state[row[0]] = state_plane

        cur.execute("DROP TABLE IF EXISTS temp_table;")
        conn.commit()
        return list_state

    def get_all_aeroplanes() -> list:
        list_airplane = []
        cur = conn.cursor()
        cur.execute("""SELECT callout FROM public.planes""")
        tmp_airplane = cur.fetchall()
        for airplane in tmp_airplane:
            list_airplane.append(airplane[0])
        conn.commit()
        return list_airplane

    def get_avg_speed():
        cur = conn.cursor()
        cur.execute("""SELECT AVG(velocity) FROM public.planes;""")
        avg_speed = cur.fetchall()
        avg_velocity = avg_speed[0][0]
        avg_velocity = round(avg_velocity, 2)
        conn.commit()
        return avg_velocity

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

    def get_aeroplanes_with_keyword(key: str) -> list:
        list_callout = []
        cur = conn.cursor()
        set = '%' + key + '%'
        cur.execute("""SELECT callout FROM public.planes WHERE callout LIKE %s;""", (set,))
        tmp_list = cur.fetchall()
        for callout in tmp_list:
            list_callout.append(callout[0])
        conn.commit()
        return list_callout
