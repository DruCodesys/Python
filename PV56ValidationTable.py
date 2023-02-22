'''
Programm um automatisch eingespeiste Messwerte zu überprüfen.
Autor: Lennart Schink
Datum: 21.02.2023
--> Keine Kopf-Aktualisierung. Versionsverfolgung erfolgt über Git und GitHub.
'''

#imports
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import os

#Dateipfad des USB-Sticks angeben. Für Entwicklungszwecke zunächst vom Root-Verzeichnis aus.
FILE = "223061_fehlerhaft.csv"
USB = "C:/Users/lschi/Documents/GitHub/Python/"
for root, dirs, files in os.walk(USB):
        for FILE in files:
            if FILE.endswith(".csv"):
                # FILE ist tabulator getrennte csv-Datei
                data = pd.read_csv(FILE, delimiter="\t", error_bad_lines= False)

                #Header sind Zeilen 0, 8, 17 --> Unregelmäßig
                #Metadaten sind in den Zeilen 1, 9, 18 --> Unregelmäßig
                idxCrack = np.arange(0,8,1) # Index für die Crack-Prüfungen
                idxFlow = np.arange(0,1,1) #Index für die Flow-Prüfungen
                SN = data['S/N']
                header = SN != 'S/N'
                data = data[header]
                date = data['S/N'][0]
                origin = data['pos'][0]
                operator = data['Crack_Pressure_Cycle1'][0]
                order = data['Crack_Pressure_Cycle2'][0]
                delivery = data['Crack_Pressure_Cycle3'][0]
                delPos = data['Crack_Pressure_Cycle4'][0]
                R1 = data['Reseat_Pressure_Cycle1']
                header = ~R1.isna()

                data = data[header]
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

                testData = pd.DataFrame()
                testData['SN'], testData['Flow'], testData['FP'] = SN, Flow, FP,
                testData['C1'], testData['R1'] = C1, R1
                testData['C2'], testData['R2'] = C2, R2
                testData['C3'], testData['R3'] = C3, R3
                testData['C4'], testData['R4'] = C4, R4
                testData['C5'], testData['R5'] = C5, R5
                testData['C6'], testData['R6'] = C6, R6
                testData['C7'], testData['R7'] = C7, R7

                val = pd.DataFrame()
                val["Cycle0"] = testData['R1'] >= testData['C1']
                val["Cycle1"] = testData['R2'] >= testData['C2']
                val["Cycle2"] = testData['R3'] >= testData['C3']
                val["Cycle3"] = testData['R4'] >= testData['C4']
                val["Cycle4"] = testData['R5'] >= testData['C5']
                val["Cycle5"] = testData['R6'] >= testData['C6']
                val["Cycle6"] = testData['R7'] >= testData['C7']
                valFlow = pd.DataFrame()
                valFlow = testData['Flow'] < 8
                valFlowPressure = testData['FP'] > 3
                errors = []
                errorIndex = []

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
                if val["Cycle0"].any():
                    for i, element in enumerate(val["Cycle0"]):
                        if element:
                            errors.append("Fehler bei Ventil No.: "+str(SN[i]) +" in Zyklus 1")
                            errorIndex.append(['Cycle0', i])
                if val["Cycle1"].any():
                    for i, element in enumerate(val["Cycle1"]):
                        if element:
                            errors.append("Fehler bei Ventil No.: " + str(SN[i]) + " in Zyklus 2")
                            errorIndex.append(['Cycle1', i])
                if val["Cycle2"].any():
                    for i, element in enumerate(val["Cycle2"]):
                        if element:
                            errors.append("Fehler bei Ventil No.: "+str(SN[i]) +" in Zyklus 3")
                            errorIndex.append(['Cycle2', i])
                if val["Cycle3"].any():
                    for i, element in enumerate(val["Cycle3"]):
                        if element:
                            errors.append("Fehler bei Ventil No.: "+str(SN[i]) +" in Zyklus 4")
                            errorIndex.append(['Cycle3', i])
                if val["Cycle4"].any():
                    for i, element in enumerate(val["Cycle4"]):
                        if element:
                            errors.append("Fehler bei Ventil No.: "+str(SN[i]) +" in Zyklus 5")
                            errorIndex.append(['Cycle4', i])
                if val["Cycle5"].any():
                    for i, element in enumerate(val["Cycle5"]):
                        if element:
                            errors.append("Fehler bei Ventil No.: "+str(SN[i]) +" in Zyklus 6")
                            errorIndex.append(['Cycle5', i])
                if val["Cycle6"].any():
                    for i, element in enumerate(val["Cycle6"]):
                        if element:
                            errors.append("Fehler bei Ventil No.: "+str(SN[i]) +" in Zyklus 7")
                            errorIndex.append(['Cycle6', i])
                print(errorIndex)
                FILE = "Ergebnis5.md"
                
                with open (FILE, 'a')as file:
                    file.write('\n______\n')
                    file.write(f" ## Messergebnise aus {origin}\n\n")
                    file.write('\n')
                    file.write(f'Aus Datei: {origin} Prüfer: {operator} Datum: {date} Auftrag: {order} Lieferschein: {delivery} Lieferscheinposition: {delPos}' )
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


