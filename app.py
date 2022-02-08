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
    return render_template('index.html', q=temp, c=umid, t=hora, graphJSON=gm())


def gm():
    temp, umid, hora = call_q()
    data = pd.DataFrame({"Tempo":hora, "Temperatura":temp, "Umidade":umid})
    data["Tempo"] = pd.to_datetime(data["Tempo"])

    fig = px.line(data, x="Tempo", y=["Temperatura", "Umidade"], markers=True)

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#E7D6D6",
        title_font_family="Montserrat",
        legend_title="Legenda",
        yaxis_title="Dados"
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))


@app.route("/pagina.html")
def pag_page():
    return render_template('pagina.html')

# https://www.youtube.com/watch?v=Qr4QMBUPxWo
# https://towardsdatascience.com/an-interactive-web-dashboard-with-plotly-and-flask-c365cdec5e3f
