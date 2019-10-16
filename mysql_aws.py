import requests
import mysql.connector
from mysql.connector import errorcode
import config
import pickle
from tqdm import tqdm

#### import the pickled data ####
data = pickle.load(open('bc_confirmed.pickle','rb'))

#### Set up the connection to AWS
cnx = mysql.connector .connect(
    host = config.host,
    user = config.user,
    passwd = config.passwd)
cursor = cnx.cursor()

#### Creating the bandcamp artist table ####
cursor.execute("""CREATE TABLE bc_artists.names_and_id (
               id int AUTO_INCREMENT,
               artist varchar(250),
               spotify_id varchar(250),
               PRIMARY KEY (id)
               )""")

def insert_artists(data):
    for artist in tqdm(data):
        sql_add = ("""INSERT INTO bc_artists.names_and_id (artist, spotify_id) VALUES (%s, %s)""")
        data_add = (artist[0],artist[1])
        cursor.execute(sql_add,data_add)
    cursor.close()
    cnx.commit()
    return

insert_artists(data)
