import random
import time
import dbrequests as dbr
import logging
import requests

level = logging.DEBUG
fmt = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(level=level, format=fmt)


def generate():
    i = 0
    celsius = 24
    umid = 70
    dbr.delete("all", "sensor")
    while True:
        celsius = celsius + random.randint(-3, 3)
        if 100 >= umid >= 0:
            umid = umid + random.randint(-5, 5)
        if umid > 100:
            umid = 100
        if umid < 0:
            umid = 0
        dbr.inserirbd(celsius, umid, "Sensor")
        time.sleep(0.5)
        i += 1
        #logging.debug(i)
        if i > 1800:
            dbr.delete(900, "sensor")
            i = 900


def sinal():
    url_temperatura = 'https://espwebsite-d81ff-default-rtdb.firebaseio.com/Sensor/murilo/temperatura.json'
    url_umidade = 'https://espwebsite-d81ff-default-rtdb.firebaseio.com/Sensor/murilo/humidade.json'
    i = 0
    dbr.delete("all", "sensor2")
    while True:
        temperatura = float(requests.get(url_temperatura).content)
        umidade = float(requests.get(url_umidade).content)
        dbr.inserirbd(temperatura, umidade, "Sensor2")
        time.sleep(2)
        i += 1
        if i > 1800:
            dbr.delete(900, "sensor2")
            i = 900





