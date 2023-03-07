'''
Programm um automatisch eingespeiste Messwerte zu überprüfen.
Autor: Lennart Schink
Datum: 21.02.2023
--> Keine Kopf-Aktualisierung. Versionsverfolgung erfolgt über Git und GitHub.
'''

import os

import pandas as pd

from Service import EvalService, DataService, errorService, TkService

# ------PROGRAMMPARAMETER-----#
# TODO: Die Variable 'USB' muss das Hauptverzeichnis des USB-Sticks sein.
USB = "C:/Users/pink_/Documents/GitHub/Python/"
#USB = "C:/Users/lschi/Documents/GitHub/Python/"
#USB = "C:\\Users\\lschi\\Desktop\\Files"
#USB = "D:\\"
# TODO: Bemessungsgrenze für Durchflusswert und Druck
DRUCK = 3
FLOW = 8

# TODO: Grenzwerte für Crack und Reseat
CRACKMAX = 2.2
CRACKMIN = 1.8
RESEATMIN = 1.6

# TODO: Name der Ergebnisdatei im .md-Format
# TODO: Bitte Beachten: DIe Ergebnisdatei manuell löschen! Dieses Script hängt immer nur an die aktuelle Datei an.
ERGEBNIS = "ErgebnisUZC.md"

#Function to handle bad line import:
def handleBadLine(badLine):
    # Remove last character (which is a tabulator) from bad lines
    if badLine[-1] == '\t':
        badLine = badLine[:-1]
    # Return the modified list of strings
    return badLine


# -----PROGRAMM-----#
# For-Schleife wird für jede Datei im Verzeichnis 'USB' ausgeführt
for root, dirs, files in os.walk(USB): #os.walk is a Generator. Not possible to store in variables once
    dirs.clear() # removes subfolders from USB-Device. So Script will only iterate in main folder
    for FILE in files:
        if FILE.endswith(".csv"):
            # FILE ist tabulator getrennte csv-Datei
            data = pd.read_csv(f"{USB}{FILE}", delimiter="\t", on_bad_lines=handleBadLine, engine='python')

            testData, SN, metaData = DataService.DataService(data)
            # Berechne boolsche Matritzen für Auswertung
            val = EvalService.evaluateCrackReseat(testData)
            valFlow = EvalService.evaluateFlow(testData, FLOW)
            valFlowPressure = EvalService.evaluateFlowPressure(testData, DRUCK)
            valCrackMax = EvalService.evaluateCrackMax(testData, CRACKMAX)
            valCrackMin = EvalService.evaluateCrackMin(testData, CRACKMIN)
            valReseatMin = EvalService.evaluateReseatMin(testData, RESEATMIN)
            errors, reds = errorService.createErrorsBySN(val, valFlow, valFlowPressure, valCrackMax, valCrackMin,
                                                         valReseatMin, SN)
            DataService.writeData(ERGEBNIS, metaData, errors, testData)
            # TkService.showNotification(errors)
            TkService.showResultsInGrid(testData, reds, metaData, errors)
