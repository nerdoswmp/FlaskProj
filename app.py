from flask import Flask, render_template, request
from dbrequests import call_q, call_minmax
from threading import Thread
import pandas as pd
import json
import plotly
import plotly.express as px
from plotly.graph_objs import *
from threading import Thread
import sender

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template('index.html')


def gm():
    temp, umid, hora = call_q("sensor")
    data = pd.DataFrame({"Tempo": hora, "Temperatura": temp, "Umidade": umid})
    data["Tempo"] = pd.to_datetime(data["Tempo"])

    fig = px.line(data, x="Tempo", y=["Temperatura", "Umidade"])

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#E7D6D6",
        title_font_family="Montserrat",
        legend_title="Legenda",
        yaxis_title="Dados",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
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

    fig2 = px.bar(data.tail(20), x="Tempo", y="Temperatura", color="Temperatura",
                  color_continuous_scale=px.colors.sequential.Teal)
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


def gm2():
    temp, umid, hora = call_q("sensor2")
    data = pd.DataFrame({"Tempo": hora, "Temperatura": temp, "Umidade": umid})
    data["Tempo"] = pd.to_datetime(data["Tempo"])

    fig = px.line(data, x="Tempo", y=["Temperatura", "Umidade"])

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#E7D6D6",
        title_font_family="Montserrat",
        legend_title="Legenda",
        yaxis_title="Dados",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
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

    fig2 = px.bar(data.tail(20), x="Tempo", y="Temperatura", color="Temperatura",
                  color_continuous_scale=px.colors.sequential.Teal)
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


@app.route("/sensor1")
def sensor1():
    maxtemp, mintemp = call_minmax("sensor")
    return render_template('sensor1.html', MaxTemp=maxtemp, MinTemp=mintemp, graphJSON=gm()[0], graphJSON2=gm()[1])


@app.route("/sensor2")
def sensor2():
    maxtemp, mintemp = call_minmax("sensor2")
    return render_template('sensor2.html', MaxTemp=maxtemp, MinTemp=mintemp, graphJSON=gm2()[0], graphJSON2=gm2()[1])


@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm()[0]


@app.route('/callback2', methods=['POST', 'GET'])
def cb2():
    return gm()[1]


@app.route('/callback3', methods=['POST', 'GET'])
def updmax():
    return str(call_minmax("sensor")[0])


@app.route('/callback4', methods=['POST', 'GET'])
def updmin():
    return str(call_minmax("sensor")[1])


@app.route('/callback5', methods=['POST', 'GET'])
def cb3():
    return gm2()[0]


@app.route('/callback6', methods=['POST', 'GET'])
def cb4():
    return gm2()[1]


@app.route('/callback7', methods=['POST', 'GET'])
def updmax2():
    return str(call_minmax("sensor2")[0])


@app.route('/callback8', methods=['POST', 'GET'])
def updmin2():
    return str(call_minmax("sensor2")[1])




@app.route("/pagina.html")
def pag_page():
    return render_template('pagina.html')

# https://www.youtube.com/watch?v=Qr4QMBUPxWo
# https://towardsdatascience.com/an-interactive-web-dashboard-with-plotly-and-flask-c365cdec5e3f


if __name__ == "__main__":
    t1 = Thread(target=sender.generate)
    t2 = Thread(target=sender.sinal)
    t1.start()
    t2.start()
    app.run(host='0.0.0.0', port=8080)
