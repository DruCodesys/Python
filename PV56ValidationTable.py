'''
Programm um automatisch eingespeiste Messwerte zu überprüfen.
Autor: Lennart Schink
Datum: 21.02.2023
--> Keine Kopf-Aktualisierung. Versionsverfolgung erfolgt über Git und GitHub.
'''

import os
from tkinter import messagebox
import pandas as pd

#------PROGRAMMPARAMETER-----#
#TODO: Die Variable 'USB' muss das Hauptverzeichnis des USB-Sticks sein.
#USB = "C:/Users/lschi/Documents/GitHub/Python/"
USB = "D:/"
#USB = "C:/Users/lschi/Desktop/Files"

#TODO: Bemessungsgrenze für Durchflusswert und Druck
DRUCK = 3
FLOW = 8
CRACKMAX = 2.2
CRACKMIN = 1.8
RESEATMIN = 1.6

#TODO: Name der Ergebnisdatei im .md-Format
#TODO: Bitte Beachten: DIe Ergebnisdatei manuell löschen! Dieses Script hängt immer nur an die aktuelle Datei an.
ERGEBNIS = "Ergebnis.md"

#-----PROGRAMM-----#
#For-Schleife wird für jede Datei im Verzeichnis 'USB' ausgeführt
for root, dirs, files in os.walk(USB):
        for FILE in files:
            if FILE.endswith(".csv"):
                # FILE ist tabulator getrennte csv-Datei
                data = pd.read_csv(FILE, delimiter="\t", on_bad_lines= 'warn')

                #Header sind Zeilen 0, 8, 17 --> Unregelmäßig
                #Metadaten sind in den Zeilen 1, 9, 18 --> Unregelmäßig
                SN = data['S/N']

                #entferne die Kopfzeilen
                header = SN != 'S/N'
                data = data[header]

                #lese meta-daten aus
                date = data['S/N'][0]
                origin = data['pos'][0]
                operator = data['Crack_Pressure_Cycle1'][0]
                order = data['Crack_Pressure_Cycle2'][0]
                delivery = data['Crack_Pressure_Cycle3'][0]
                delPos = data['Crack_Pressure_Cycle4'][0]

                #entferne die Zeilen mit Metadaten
                R1 = data['Reseat_Pressure_Cycle1']
                header = ~R1.isna()
                data = data[header]

                #Konvertiere die Datentypen string -> double/int in numpy - Array
                Flow = data['Flow'].to_numpy(dtype='double')
                FP = data['Flow_Pressure'].to_numpy(dtype='double')
                SN = data['S/N'].to_numpy(dtype='int')
                pos = data['pos']
                C1 = data['Crack_Pressure_Cycle1'].to_numpy(dtype='double')
                C2 = data['Crack_Pressure_Cycle2'].to_numpy(dtype='double')
                C3 = data['Crack_Pressure_Cycle3'].to_numpy(dtype='double')
                C4 = data['Crack_Pressure_Cycle4'].to_numpy(dtype='double')
                C5 = data['Crack_Pressure_Cycle5'].to_numpy(dtype='double')
                C6 = data['Crack_Pressure_Cycle6'].to_numpy(dtype='double')
                C7 = data['Crack_Pressure_Cycle7'].to_numpy(dtype='double')
                R1 = data['Reseat_Pressure_Cycle1'].to_numpy(dtype='double')
                R2 = data['Reseat_Pressure_Cycle2'].to_numpy(dtype='double')
                R3 = data['Reseat_Pressure_Cycle3'].to_numpy(dtype='double')
                R4 = data['Reseat_Pressure_Cycle4'].to_numpy(dtype='double')
                R5 = data['Reseat_Pressure_Cycle5'].to_numpy(dtype='double')
                R6 = data['Reseat_Pressure_Cycle6'].to_numpy(dtype='double')
                R7 = data['Reseat_Pressure_Cycle7'].to_numpy(dtype='double')

                #Erstelle Datenframe aus numpy-Spalten
                testData = pd.DataFrame()
                testData['SN'], testData['Flow'], testData['FP'] = SN, Flow, FP
                testData['C1'] = C1
                testData['C2'] = C2
                testData['C3'] = C3
                testData['C4'] = C4
                testData['C5'] = C5
                testData['C6'] = C6
                testData['C7'] = C7
                testData['R1'] = R1
                testData['R2'] = R2
                testData['R3'] = R3
                testData['R4'] = R4
                testData['R5'] = R5
                testData['R6'] = R6
                testData['R7'] = R7

                #Berechne die Felder in denen Der Reseat-Pressure größer oder gleich dem Crack-Pressure ist
                val = pd.DataFrame()
                val["Cycle0"] = (testData['R1'] >= testData['C1'])
                val["Cycle1"] = (testData['R2'] >= testData['C2'])
                val["Cycle2"] = (testData['R3'] >= testData['C3'])
                val["Cycle3"] = (testData['R4'] >= testData['C4'])
                val["Cycle4"] = (testData['R5'] >= testData['C5'])
                val["Cycle5"] = (testData['R6'] >= testData['C6'])
                val["Cycle6"] = (testData['R7'] >= testData['C7'])

                #Berechne die Felder in denen max. der Crack/Pressure [berschritten wurde
                valCMax = pd.DataFrame()
                valCMax["Cycle0"] = testData['C1'] > CRACKMAX
                valCMax["Cycle1"] = testData['C2'] > CRACKMAX
                valCMax["Cycle2"] = testData['C3'] > CRACKMAX
                valCMax["Cycle3"] = testData['C4'] > CRACKMAX
                valCMax["Cycle4"] = testData['C5'] > CRACKMAX
                valCMax["Cycle5"] = testData['C6'] > CRACKMAX
                valCMax["Cycle6"] = testData['C7'] > CRACKMAX

                #Berechne die Felder in denen der Crack/Pressure zu klein ist.
                valCMin = pd.DataFrame()
                valCMin["Cycle0"] = testData['C1'] < CRACKMIN
                valCMin["Cycle1"] = testData['C2'] < CRACKMIN
                valCMin["Cycle2"] = testData['C3'] < CRACKMIN
                valCMin["Cycle3"] = testData['C4'] < CRACKMIN
                valCMin["Cycle4"] = testData['C5'] < CRACKMIN
                valCMin["Cycle5"] = testData['C6'] < CRACKMIN
                valCMin["Cycle6"] = testData['C7'] < CRACKMIN

                #BErechne die Felder in denenn der nReseat-Pressure zu klein ist
                valRmin = pd.DataFrame()
                valRmin["Cycle0"] = testData['R1'] < RESEATMIN
                valRmin["Cycle1"] = testData['R2'] < RESEATMIN
                valRmin["Cycle2"] = testData['R3'] < RESEATMIN
                valRmin["Cycle3"] = testData['R4'] < RESEATMIN
                valRmin["Cycle4"] = testData['R5'] < RESEATMIN
                valRmin["Cycle5"] = testData['R6'] < RESEATMIN
                valRmin["Cycle6"] = testData['R7'] < RESEATMIN

                #Berechne die Felder in denen der Flow kleiner FLOW und Druck größer DRUCK ist.
                valFlow = pd.DataFrame()
                valFlow = testData['Flow'] < FLOW
                valFlowPressure = testData['FP'] > DRUCK

                #Initialisiere Fehler-Array und schreibe die Fehler und Fehlerindizes in die Arrays
                errors = []
                errorIndex = []
                cycles = ["Cycle0", "Cycle1", "Cycle2", "Cycle3", "Cycle4", "Cycle5", "Cycle6"]
                if valFlowPressure.any():
                    for i, element in enumerate(valFlowPressure):
                        if element:
                            errors.append("Fehler bei Ventil No.: "+ str(SN[i]) +" im Flow-Druck")
                            errorIndex.append(['FP', i])
                if valFlow.any():
                    for i, element in enumerate(valFlow):
                        if element:
                            errors.append("Fehler bei Ventil No.: " + str(SN[i]) + " im Flow")
                            errorIndex.append(['Flow', i])
                for cycle in cycles:
                    if val[cycle].any():
                        for i, element in enumerate(val[cycle]):
                            if element:
                                errors.append("Fehler bei Ventil No.: "+str(SN[i]) +"in Zyklus" + str(cycles.index(cycle)+1))
                                errorIndex.append([cycle, i])
                    if valCMax[cycle].any():
                        for i, element in enumerate(valCMax[cycle]):
                            if element:
                                errors.append("Fehler bei Ventil No.: "+str(SN[i]) +"in Zyklus" + str(cycles.index(cycle)+1)+ "Crack-Pressure zu hoch!")
                                errorIndex.append([cycle, i])
                    if valCMin[cycle].any():
                        for i, element in enumerate(valCMin[cycle]):
                            if element:
                                errors.append("Fehler bei Ventil No.: "+str(SN[i]) +"in Zyklus" + str(cycles.index(cycle)+1)+ "Crack-Pressure zu niedrig!")
                                errorIndex.append([cycle, i])
                    if valRmin[cycle].any():
                        for i, element in enumerate(valRmin[cycle]):
                            if element:
                                errors.append("Fehler bei Ventil No.: "+str(SN[i]) +"in Zyklus" + str(cycles.index(cycle)+1)+ "Reseat-Pressure zu niedrig!")
                                errorIndex.append([cycle, i])

                print(errorIndex)
                FILE = ERGEBNIS

                with open (FILE, 'a')as file:
                    file.write('\n______\n')
                    file.write(f" ## Messergebnise aus {origin}\n\n")
                    file.write('\n')
                    file.write(f"Aus Datei: {origin} Prüfer: {operator} Datum: {date} Auftrag: {order} Lieferschein: {delivery} Lieferscheinposition: {delPos}")
                    file.write('\n\n')
                    file.close()
                testData.to_markdown(FILE, mode = 'a')
                with open(FILE, 'a' ) as file:
                    file.write("\n")
                    for element in errors:
                        file.write("\n"+element+"\n")
                    file.write("\n")
                    file.close()

                if len(errors) == 0:

                    messagebox.showinfo("KEIN FEHLER", "Es wurden keine Fehler in den Messungen gefunden")

                else:
                    messagebox.showwarning("FEHLER IN DEN MESSUNGEN", "Es wurden Fehler in den Messungen gefunden. Öffne die Datei result.md um anzuzeigen")


