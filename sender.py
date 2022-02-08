import random
import time
import requests
import pyodbc

i = 1


def InserirBD(c, u):
    server = 'DESKTOP-GGRN2GL'
    database = 'debug'
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cursor.execute(f"INSERT dbo.Sensor (Temperatura, Umidade) VALUES ({c},{u});")
    cursor.commit()
    print("Inserido com sucesso!")


while True:
    celsius = random.randint(0, 35)
    umid = random.randint(0, 100)
    InserirBD(celsius, umid)
    time.sleep(30)
