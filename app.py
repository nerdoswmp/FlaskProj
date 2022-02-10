from flask import Flask, render_template, request
import pandas as pd
import json
import pyodbc
import plotly
import plotly.express as px
from plotly.graph_objs import *

app = Flask(__name__)


def call_q():
    server = 'DESKTOP-GGRN2GL' # Tenta não esquecer de mudar isso antes de rodar o flask
    database = 'debug'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
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

    return temp, umid, hora


@app.route("/")
def home_page():
    temp, umid, hora = call_q()
    return render_template('index.html', q=temp, c=umid, t=hora, graphJSON=gm()[0], graphJSON2=gm()[1])


def gm():
    temp, umid, hora = call_q()
    data = pd.DataFrame({"Tempo":hora, "Temperatura":temp, "Umidade":umid})
    data["Tempo"] = pd.to_datetime(data["Tempo"])

    fig = px.line(data, x="Tempo", y=["Temperatura", "Umidade"])

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#E7D6D6",
        title_font_family="Montserrat",
        legend_title="Legenda",
        yaxis_title="Dados"
    )

    """ 
    xaxis_tickformatstops=[
        dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
        dict(dtickrange=[1000, 60000], value="%H:%M:%S m"),
        dict(dtickrange=[60000, 3600000], value="%H:%M h"),
        dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
        dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
        dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
        dict(dtickrange=["M1", "M12"], value="%b '%y M"),
        dict(dtickrange=["M12", None], value="%Y Y")
    ] 
    """

    fig2 = px.bar(data.tail(20), x="Tempo", y="Temperatura", color="Temperatura")
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#E7D6D6",
        title_font_family="Montserrat",
        legend_title="Legenda",
        yaxis_title="Dados"
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON, graphJSON2


@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))


@app.route("/pagina.html")
def pag_page():
    return render_template('pagina.html')

# https://www.youtube.com/watch?v=Qr4QMBUPxWo
# https://towardsdatascience.com/an-interactive-web-dashboard-with-plotly-and-flask-c365cdec5e3f
#
