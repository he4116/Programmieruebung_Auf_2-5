

# Paket für Bearbeitung von Tabellen
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
# Paket
## zuvor !pip install plotly
## ggf. auch !pip install nbformat
import plotly.io as pio
pio.renderers.default = "browser"



def read_my_csv():
    # Einlesen eines Dataframes
    ## "\t" steht für das Trennzeichen in der txt-Datei (Tabulator anstelle von Beistrich)
    ## header = None: es gibt keine Überschriften in der txt-Datei
    df = pd.read_csv("data/activities/activity.csv")
    time = np.arange(0, len(df))
    df["Time"] = time 
    

    # Setzt die Columnnames im Dataframe
    #df.columns = ["Duration","Distance","OriginalPace","HeartRate","Cadence","PowerOriginal","CalculatedPace","CalculatedStrideLength","CalculatedAerobicEfficiencyPace","CalculatedAerobicEfficiencyPower","CalculatedEfficiencyIndex"]
    
    # Gibt den geladen Dataframe zurück
    return df






def make_plot(df):

    # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
    fig = px.line(df, x="Time", y=["PowerOriginal", "HeartRate"])
    return fig


def get_zone_limits(max_hr): 
    return {
        "Zone 1": [0.5 * max_hr, 0.6 * max_hr],
        "Zone 2": [0.6 * max_hr, 0.7 * max_hr],
        "Zone 3": [0.7 * max_hr, 0.8 * max_hr],
        "Zone 4": [0.8 * max_hr, 0.9 * max_hr],
        "Zone 5": [0.9 * max_hr, max_hr]}


def berechne_zonen(hr_series, max_hr):
    
    zones = []
    for hr in hr_series:
        if hr < 0.6 * max_hr:
            zones.append("Zone 1")
        elif hr < 0.7 * max_hr:
            zones.append("Zone 2")
        elif hr < 0.8 * max_hr:
            zones.append("Zone 3")
        elif hr < 0.9 * max_hr:
            zones.append("Zone 4")
        else:
            zones.append("Zone 5")
    return zones


def zone_plot(df, max_hr):
    df = df.copy()
    df["Zone"] = berechne_zonen(df["HeartRate"], max_hr)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Time"],
        y=df["HeartRate"],
        mode='lines',
        name='Heart Rate',
        line=dict(color='blue')
    ))

    return fig
    





if __name__ == "__main__":
    df = read_my_csv()
    print(df.head())

    #fig = make_plot(df)
    #fig.show()
    max_hr = df["HeartRate"].max()
    #print("Max Heart Rate:", max_hr)
    zone_dict = get_zone_limits(max_hr)
    #print(zone_dict)
    fig = zone_plot(df, max_hr)
    fig.show()
