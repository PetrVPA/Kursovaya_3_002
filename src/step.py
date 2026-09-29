import requests
import psycopg2
import os.path
from dotenv import load_dotenv
from work import APIState
from work import APIAirplane

load_dotenv('../.env')
word = os.getenv('PASWORD')

conn = psycopg2.connect(
    host = "localhost",
    database = "airplanes_country",
    port = 5432,
    user = "postgres",
    #pasword = word
    password = "12345"
)

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
    print(F"{kontr_st} таблица создана")
    if kontr_st == False:
        cur.execute("""CREATE TABLE countries (title VARCHAR(50) PRIMARY KEY)""")
    cur.execute("""SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'planes')""")
    kontr_air = cur.fetchone()[0]
    if kontr_air == False:
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
    if callout != None:
        velocity = plane_data[9]
        if velocity != None:
            true_track = plane_data[10]
            if true_track != None:


                country_title = country
                cur = conn.cursor()
                cur.execute("""INSERT INTO planes (callout, velocity, true_track, country_title) VALUES (%s, %s, %s, %s)""",
                (callout, velocity, true_track, country_title))
    conn.commit()

state = APIState()
airplane = APIAirplane()

if __name__ == '__main__':

    creat_tables()

    for country in countries:
        bbox = state.get_coordinates(country)
        print(bbox)
        plane_box = airplane.get_coordinates(bbox)
        planes = plane_box.get('states')
        #print(planes)
        save_country_data_to_db(country)
        for plane in planes:
            save_planes_data_to_db(country, plane)