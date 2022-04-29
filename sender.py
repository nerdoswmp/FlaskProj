import random
import time
import dbrequests as dbr
import pyodbc

i = 1799
celsius = 24
umid = 70


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
    celsius = celsius + random.randint(-3, 3)
    if 100 >= umid >= 0:
        umid = umid + random.randint(-5, 5)
    if umid > 100:
        umid = 100
    if umid < 0:
        umid = 0
    InserirBD(celsius, umid)
    time.sleep(2)
    i += 1
    print(i)
    if i > 1800:
        dbr.delete()
        i = 900
