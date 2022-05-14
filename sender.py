import random
import time
import dbrequests as dbr
import logging


def generate():
    level = logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)

    i = 0
    celsius = 24
    umid = 70
    dbr.delete("all")
    while True:
        celsius = celsius + random.randint(-3, 3)
        if 100 >= umid >= 0:
            umid = umid + random.randint(-5, 5)
        if umid > 100:
            umid = 100
        if umid < 0:
            umid = 0
        dbr.inserirbd(celsius, umid)
        time.sleep(0.5)
        i += 1
        #logging.debug(i)
        if i > 1800:
            dbr.delete(900)
            i = 900






