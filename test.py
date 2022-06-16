from firebase import firebase
import json
import dbrequests as dbr
from threading import Thread
import sender as send
import requests
import pandas as pd
import time

auth = firebase.FirebaseAuthentication("dldVHFtk6iAETN7a1GdmXN0ARyAAKRehdyHkNeBe", "nerdoswampo@gmail.com")
firebase = firebase.FirebaseApplication("https://espwebsite-d81ff-default-rtdb.firebaseio.com", auth)


def sensor1():
    t1 = Thread(target=send.generate)
    t1.start()
    temp, umid, hora = dbr.call_q("sensor")
    data = {'temp':temp, 'umid':umid, 'time':hora}
    print(data["temp"])
    firebase.post('sensor1send/', data)
    get = firebase.get('sensor1send/', "")
    key = list(get.keys())[0]
    while True:
        temp, umid, hora = dbr.call_q("sensor")
        data = {'temp': temp, 'umid': umid, 'time': hora}
        firebase.put(f'sensor1send/{key}', {"temp", "umid", "time"}, data)
        time.sleep(30)


def sensor2():
    t1 = Thread(target=send.sinal)
    t1.start()
    temp, umid, hora = dbr.call_q("sensor2")
    data = {'temp':temp, 'umid':umid, 'time':hora}
    print(data["temp"])
    firebase.post('sensor2send/', data)
    get = firebase.get('sensor2send/', "")
    key = list(get.keys())[0]
    while True:
        temp, umid, hora = dbr.call_q("sensor2")
        data = {'temp': temp, 'umid': umid, 'time': hora}
        firebase.put(f'sensor2send/{key}', {"temp", "umid", "time"}, data)
        time.sleep(30)
