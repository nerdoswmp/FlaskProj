import pyodbc
import logging

level = logging.DEBUG
fmt = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(level=level, format=fmt)

server = 'DESKTOP-GGRN2GL'
database = 'debug'


def inserirbd(c, u):
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cursor.execute(f"INSERT dbo.Sensor (Temperatura, Umidade) VALUES ({c},{u});")
    cursor.commit()
    logging.info("Inserido com sucesso!")
    cnxn.close()


def call_q():
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cursor.execute("SELECT Temperatura, Umidade, timestamp FROM dbo.Sensor")
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


def call_minmax():
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cursor.execute("select Max(Temperatura), Min(Temperatura) from dbo.sensor")
    row = cursor.fetchone()
    maxtemp = row[0]
    mintemp = row[1]
    cnxn.close()
    return maxtemp, mintemp


def delete(amount):
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    if amount == "all":
        cursor.execute(f"DELETE FROM dbo.Sensor")
        cursor.commit()
        return logging.info("\n\nTodos itens removidos do banco")

    cursor.execute(f"DELETE TOP ({amount}) FROM dbo.Sensor")
    cursor.commit()
    cnxn.close()
    return logging.info("\n\n900 itens removidos do banco")

