import random
import time
import dbrequests as dbr
import pyodbc
import logging

level = logging.DEBUG
fmt = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(level=level, format=fmt)

i = 0
celsius = 24
umid = 70


def inserirbd(c, u):
    server = 'DESKTOP-GGRN2GL'
    database = 'debug'
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cursor.execute(f"INSERT dbo.Sensor (Temperatura, Umidade) VALUES ({c},{u});")
    cursor.commit()
    logging.info("Inserido com sucesso!")


while True:
    celsius = celsius + random.randint(-3, 3)
    if 100 >= umid >= 0:
        umid = umid + random.randint(-5, 5)
    if umid > 100:
        umid = 100
    if umid < 0:
        umid = 0
    inserirbd(celsius, umid)
    time.sleep(0.5)
    i += 1
    logging.debug(i)
    if i > 1800:
        dbr.delete()
        i = 900
