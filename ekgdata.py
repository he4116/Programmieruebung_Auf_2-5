import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        #pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])

    @staticmethod
    def load_by_id(ekg_list, ekg_id):
        for ekg in ekg_list:
            if ekg["id"] == ekg_id:
                return ekg
        return None

    def find_peaks(self, threshold, respacing_factor):


        # Respace the series
        series = self.df["Messwerte in mV"].iloc[::respacing_factor]
        

        # Filter the series
        series = series[series > threshold]

        peaks = []
        last = 0
        current = 0
        next = 0

        for index, row in series.items():
            last = current
            current = next
            next = row

            if last < current and current > next and current > threshold:
                peaks.append(index - respacing_factor)
                #if 0<= index <2000:
                    #peaks.append(current)
            
            self.df.loc[:, "is_peak"] = False
            self.df.loc[peaks, "is_peak"] = True
            self.df.loc[:, "is_peak"] = False
            self.df.loc[peaks, "is_peak"] = True

        return peaks
    
    
    def estimate_hr(self, peaks):
        heart_rates = []
        zeit_in_ms = self.df["Zeit in ms"]
        for i in range(len(peaks)-1):
            interval = zeit_in_ms.iloc[peaks[i+1]]-zeit_in_ms.iloc[peaks[i]]
            if interval > 0:
                bpm = 60000 / interval
                heart_rates.append(bpm)
        avg_heart_rate = sum(heart_rates) / len(heart_rates) if heart_rates else 0
        return avg_heart_rate

    def plot_time_series(self, peaks):

        
        peak_times = self.df.loc[peaks, "Zeit in ms"].tolist()
        peak_values = self.df.loc[peaks, "Messwerte in mV"].tolist()

        
        self.fig = px.line(self.df, x="Zeit in ms", y="Messwerte in mV")
        self.fig.add_trace(go.Scatter(
            x=peak_times,
            y=peak_values,
            mode='markers',
            marker=dict(color='red', size=8),
            name='Peaks'))
        zeit_start = self.df["Zeit in ms"][0]
        self.fig.update_layout(xaxis=dict(range=[zeit_start, (zeit_start+30000)]))
        return self.fig 

if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][1]
    print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    print(ekg.df.head())
    fig = ekg.plot_time_series()
    fig.show()
    
