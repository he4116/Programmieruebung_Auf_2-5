# Programmieruebung_Auf_2-5
Programmieraugaben 2-5
## Aufgabe 2
Einführung Streamlit - Übungen  

## Aufgabe 3 
Die Datenauswertung mit Pandas wird vertieft. Zuerst wurde in den Notebooks gelesen und uns eingearbeitet, indem wir die Übungen neu gecodet haben. Ziel der Aufgabe ist es erstmals einen interaktiven Plot zu erstellen. 
Dazu haben wir in dem Repository weitergearbeitet und die Daten zunächst in einem Notebook analysiert. Wir haben die Daten aus der activity.csv in einem Pandas DataFrame geladen. Aus den Daten haben wir den Mittelwert der Leistung gebildet, den Maximalwert der Leistung, und den Mittelwert der Herzfrequenz. Dann haben wir die Leistung und die Herzfrequenz über die Zeit geplottet in einem interaktiven Plot. 
Aus dem Datensatz haben wir die Daten in fünf Zonen (Herzfrequenz) geteilt und diese auch als Plot über dem anderen Plot dargestellt. Daraus kann man sehen, wie viel Zeit in welcher Zone verbracht wurde, indem sogar die maximale Herfrequenz mittels einem Button (- und +) verändert werden kann. Darunter befindet sich ein Fenster mit der durschnittlichen Leistung in den Zonen. 

![alt text](image.png)
![alt text](<Screenshot 2025-06-04 220542.png>)
![alt text](<Screenshot 2025-06-04 220533.png>)
![alt text](<Screenshot 2025-06-04 220504.png>)

## Aufgabe 4 
Die Aufgabe war, dass eine Leistungskurve erstellt wird basierend auf den Leistungsdaten in Watt und der Zeit in Minuten oder Sekunden. Es wird ein Algorithmus geschrieben, welcher die Peaks in einem EKG-Signal findet, um daraus die Herzfrequenz zu bestimmen. Dabei soll die Funktion für alle Leistungen in Watt anwendbar sein, die als Serie oder numpy-Array vorliegen. 
Zunächst haben wir ein Dataframe erstellt, was die Leistung und die Zeit enthält. Daraus haben wir im Anschluss einen Plot erstellt, der die PowerCurve darstellt. 
 