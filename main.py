import streamlit as st
from read_data import load_person_data
from read_data import get_person_list
from PIL import Image #paket zum anzeigen der bilder
from read_data import find_person_data_by_name
from read_pandas import read_my_csv
from read_pandas import make_plot
from read_pandas import get_zone_limits
from read_pandas import zone_plot
from read_pandas import data_zones
from person import Person
from ekgdata import EKGdata


tab1, tap2 = st.tabs(["Versuchsperson", "Daten"])

with tab1:
#funktionen müssen ienmal importiert werden zum aufrufen
    person_data = load_person_data()
    person_names = get_person_list(person_data)


    st.write("# EKG_App")
    st.write("## Versuchsperson auswählen")

# Session State wird leer angelegt, solange er noch nicht existiert
    if 'current_user' not in st.session_state:
        st.session_state.current_user = 'None'

# Dieses Mal speichern wir die Auswahl als Session State
    st.session_state.current_user = st.selectbox(
        'Versuchsperson',
        options = person_names, key="sbVersuchsperson")

    st.write("Der Name ist: ", st.session_state.current_user) 

    person = find_person_data_by_name(st.session_state.current_user)


    image = Image.open(person["picture_path"])
    # Anzeigen eines Bilds mit Caption
    st.image(image, caption=st.session_state.current_user)

    my_currrent_person = Person(person)
    st.write("Geburtsdatum: ", my_currrent_person.date_of_birth)
    st.write("ID: ", my_currrent_person.id)
    st.write("Alter: ", Person.calc_age(my_currrent_person.date_of_birth))
    st.write("max. Herzfrequenz basierend auf Geschecht und Alter: ", my_currrent_person.calc_max_heart_rate())

    #threshold = 340
    #respacing_factor = 5

    # Dropdown-Liste für EKG-Tests
    ekg_tests = person.get('ekg_tests', [])
    ekg_ids = [test['id'] for test in ekg_tests]
    selected_ekg_id = st.selectbox("Wähle eine EKG-Test-ID aus:", ekg_ids)
    ekg_dict = EKGdata.load_by_id(ekg_tests, selected_ekg_id)
    ekg = EKGdata(ekg_dict)

    fig = ekg.plot_time_series()
    st.plotly_chart(fig, use_container_width=True)

with tap2:
    st.write("## EKG-Daten")
    st.write("Hier werden die EKG-Daten angezeigt.")

    df = read_my_csv()
    fig = make_plot(df)
    st.plotly_chart(fig, use_container_width=True)

    st.write("Maximale Leistung: ", int(df["PowerOriginal"].max()))
    st.write("Durchschnittliche Leistung: ", int(df["PowerOriginal"].mean()))
    

    st.number_input("Geben Sie die maximale Herzfrequenz ein:",value= int(df["HeartRate"].mean()) , key="max_hr")

    max_hr = st.session_state.max_hr	
    zone_dict = get_zone_limits(max_hr)
    fig = zone_plot(df, max_hr)
    st.plotly_chart(fig, use_container_width=True)

    zone_df = data_zones(df, max_hr)
    st.write("Zeit in den Zonen:")
    st.dataframe(zone_df)