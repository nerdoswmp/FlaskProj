import pyodbc
import logging
from firebase import firebase

level = logging.DEBUG
fmt = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(level=level, format=fmt)
auth = firebase.FirebaseAuthentication("dldVHFtk6iAETN7a1GdmXN0ARyAAKRehdyHkNeBe", "nerdoswampo@gmail.com")
firebase = firebase.FirebaseApplication("https://espwebsite-d81ff-default-rtdb.firebaseio.com", auth)
server = 'DESKTOP-GGRN2GL'
database = 'debug'


def inserirbd(c, u, db):

    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cursor.execute(f"INSERT dbo.{db} (Temperatura, Umidade) VALUES ({c},{u});")
    cursor.commit()
    # logging.info("Inserido com sucesso!")
    cnxn.close()


def call_q(db):
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cursor.execute(f"SELECT Temperatura, Umidade, timestamp FROM dbo.{db}")
    row = cursor.fetchone()
    temp = []
    umid = []
    hora = []
    while row:
        temp.append(row[0])
        umid.append(row[1])
        hora.append(str(row[2]))
        row = cursor.fetchone()
    cnxn.close()
    return temp, umid, hora


def call_minmax(db):
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cursor.execute(f"select Max(Temperatura), Min(Temperatura) from dbo.{db}")
    row = cursor.fetchone()
    maxtemp = row[0]
    mintemp = row[1]
    cnxn.close()
    return maxtemp, mintemp


def delete(amount, db):
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    if amount == "all":
        cursor.execute(f"DELETE FROM dbo.{db}")
        cursor.commit()
        return logging.info("\n\nTodos itens removidos do banco")

    cursor.execute(f"DELETE TOP ({amount}) FROM dbo.{db}")
    cursor.commit()
    cnxn.close()
    return logging.info("\n\n900 itens removidos do banco")


def firebaseget(sensor):
    if sensor == "sensor":
        get = firebase.get('sensor1send/', "")
        key = list(get.keys())[0]
        table = list(firebase.get(f'sensor1send/{key}', "").keys())[3]
        #print(key)
        data = firebase.get(f"/sensor1send/{key}/{table}", "")
        #/sensor1send/-N4ewyhqkEqWOc6bzoKz/{'time', 'umid', 'temp'}
        return data

    elif sensor == "sensor2":
        get = firebase.get('sensor2send/', "")
        key = list(get.keys())[0]
        table = list(firebase.get(f'sensor2send/{key}', "").keys())[3]
        # print(key)
        data = firebase.get(f"/sensor2send/{key}/{table}", "")
        #/sensor2send/-N4esE97pT0Ru-uoN93A/{'temp', 'time', 'umid'}
        return data
