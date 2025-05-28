

# Paket für Bearbeitung von Tabellen
import pandas as pd
import numpy as np
import plotly.express as px
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
    zone_1 =[0.5 * max_hr, 0.6 * max_hr]
    zone_2 = [0.6 * max_hr, 0.7 * max_hr]
    zone_3 = [0.7 * max_hr, 0.8 * max_hr]
    zone_4 = [0.8 * max_hr, 0.9 * max_hr]
    zone_5 = [0.9 * max_hr, max_hr]
    zone_dict = {
        "Zone 1": zone_1,
        "Zone 2": zone_2,
        "Zone 3": zone_3,
        "Zone 4": zone_4,
        "Zone 5": zone_5
    }   
    return zone_dict

def zone_plot(df, max_hr):
    # Berechne Herzfrequenz-Zonen
    zones = get_zone_limits(max_hr)

    # Plot mit Herzfrequenz über Zeit
    fig = px.line(df, x="Time", y=["HeartRate", "PowerOriginal"], title="Herzfrequenz über Zeit",
                  labels={"Time": "Zeit (s)", "HeartRate": "Herzfrequenz (bpm)"})

    # Füge farbige Zonen als horizontale Bänder hinzu
    for zone_name, (lower, upper) in zones.items():
        fig.add_shape(
            type="rect",
            x0=df["Time"].min(), x1=df["Time"].max(),
            y0=lower, y1=upper,
            fillcolor=_zone_color(zone_name),  # siehe Funktion unten
            opacity=0.2,
            layer="below",
            line_width=0)
    
    return fig

# Farben für die Zonen definieren
def _zone_color(zone_name):
    colors = {
        "Zone 1": "lightblue",
        "Zone 2": "lightgreen",
        "Zone 3": "yellow",
        "Zone 4": "orange",
        "Zone 5": "red"
    }
    return colors.get(zone_name, "gray")




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
