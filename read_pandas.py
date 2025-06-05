

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

    fig = px.scatter(df, x="Time", y="HeartRate", color="Zone")

    color = {
        "Zone 1": "blue",
        "Zone 2": "green",
        "Zone 3": "yellow",
        "Zone 4": "orange",
        "Zone 5": "red"
    }

    # Linie für PowerOriginal hinzufügen
    fig.add_trace(go.Scatter(
        x=df["Time"],
        y=df["PowerOriginal"],
        mode="lines",
        name="PowerOriginal",
        line=dict(color="black", width=1)
    ))

    return fig

def data_zones(df, max_hr):
    df = df.copy()
    df["Zone"] = berechne_zonen(df["HeartRate"], max_hr)

    # Berechnung der Zeit in jeder Zone
    zone_times = df.groupby("Zone").size() * (1 / 60)  # Zeit in Minuten
    zone_averagePower = df.groupby("Zone")["PowerOriginal"].mean()

    # Erstellen eines DataFrames für die Anzeige
    zone_df = pd.DataFrame({
        "Time (min)": zone_times,
        "Average Power (W)": zone_averagePower
    }).reset_index()
    return zone_df








#Power Curve
df = read_my_csv()
series = df["PowerOriginal"]


def find_best_effort(series, Windowsize):
    """Finds the best effort in a series of power values."""
    best_effort = 0
    for i in range(len(series) - Windowsize + 1):
        current_effort = series[i:i + Windowsize].mean()
        if current_effort > best_effort:
            best_effort = current_effort
    return best_effort

Windowsize = [10,30, 60, 120, 300, 600, 900, 1800, 3600]  # in seconds
def create_power_curve(series, Windowsize):
    """Creates a power curve based on the best efforts over different window sizes."""
    power_curve = []
    for window in Windowsize:
        best_effort = find_best_effort(series, window)
        power_curve.append(best_effort)
    power_curve_df = pd.DataFrame({
       "Time (s)": Windowsize,
       "Best Effort (W)": power_curve
    })

    return power_curve_df


# plot der PowerCurve
def plot_power_curve(power_curve_df):
    """Plots the power curve."""
    power_curve_df = power_curve_df.copy()
    power_curve_df["Time (min)"] = power_curve_df["Time (s)"] / 60
    fig = px.line(power_curve_df , x="Time (min)", y="Best Effort (W)", markers=True)
    #fig.update_layout(xaxis_title="Time (s)", yaxis_title="Best Effort (W)")
    #speichern des Plots als Bild
    fig.write_image("power_curve.png")
    return fig



if __name__ == "__main__":
    df = read_my_csv()
    print(df.head())

    #fig = make_plot(df)
    #fig.show()
    max_hr = df["HeartRate"].max()
    #print("Max Heart Rate:", max_hr)
   # zone_dict = get_zone_limits(max_hr)
    #print(zone_dict)
    #fig = zone_plot(df, max_hr)
    #fig.show()
    #zone_df = data_zones(df, max_hr)
    #print(zone_df)

    #print("Best Effort:", find_best_effort(series, Windowsize=60))
    pow_df = create_power_curve(series, Windowsize)
    print("Power Curve:", pow_df)
    fig = plot_power_curve(pow_df)
    fig.show()
    
    