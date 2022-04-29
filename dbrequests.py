import pyodbc

server = 'DESKTOP-GGRN2GL'
database = 'debug'


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


def delete():
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cursor.execute("DELETE TOP (900) FROM dbo.Sensor")
    cursor.commit()
    print("\n\n900 items removidos do banco")
    cnxn.close()
