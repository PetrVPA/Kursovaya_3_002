import requests
import psycopg2
import os.path
from dotenv import load_dotenv

load_dotenv('../.env')
word = os.getenv('PASWORD')

conn = psycopg2.connect(
    host = "localhost",
    database = "airplanes_country",
    port = 5432,
    user = "postgres",
    pasword = word
)

countries = [
    "Germany",
	"France",
	"Poland",
	"Norway"
]

def creat_tables():
    cur = conn.cursor()
    cur.execute("""CREATE TABLE countres (title VARCHAR(50) PRIMARY KEY;""")
    cur.execute("""CREATE TABLE planes (
                id INT PRIMARY KEY,
                calsing VARCHAR(50) NOT NULL,
                velocity FLOAT NOT NULL,                
                true_track FLOAT NOT NULL,
                country_title VARCHAR(50),
                CONSTRAINT FK_CounryPlane
                FOREIGN KEY (country_title) REFERENCES countries(title)
    
            );""")
    conn.commit()

def get_nominatim_data(country: str)-> list[str]:
    
    response = requests.get(
        "http://npminatim.openstreetmap.org/search",
        params = {
            "q": country,
            "format": "json2",
            "limit": 1,
        },
        headers={"User-Agent": "FlightTracker/1.0"},
    )
        
    data = response.json()[0]
    print(data)
        
    bbox = data["boudingbox"]
    return bbox
    
def get_opensky_data(bbox: list[int]) -> list[str]:
     
    planes = requests.get(
        "http://opensky-network.org/api/states/all",
        params = {
            "lamin": bbox[0],
            "lamax": bbox[1],
            "lomin": bbox[2],
            "lomax": bbox[3],
        },
    ).json()
    return planes["states"]
    
def save_country_data_to_db(country: str):
    cur = conn.cursor()
    cur.execute("""INSERT INTO countries (title) VALUES (%s)""", (country))
    conn.commit()
    
def save_planes_data_to_db(country: str, plane_data: list):
    
    calsing = plane_data[1]
    velocity = plane_data[9]
    true_track = plane_data[10]
    country_title = country
    
    cur = conn.cursor()
    cur.execute("""INSERT INTO planes (calsing, velocity, true_track, country_title) VALUES (%s, %s, %s, %s)""", (calsing, velocity, true_track, country_title))
    conn.commit()
            
#def main():

if __name__ == '__main__':
    creat_tables()
    
    for country in countries:
        bbox = get_nominatim_data(country)
        planes = get_opensky_data(bbox)
        save_country_data_to_db(country)
        for plane in planes:
            save_planes_data_to_db(country, plane)
    