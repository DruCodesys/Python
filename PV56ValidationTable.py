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
USB = "C:/USers/pink_/Documents/GitHub/Python/"
# USB = "C:/Users/lschi/Documents/GitHub/Python/"
# USB = "D:/"

# TODO: Bemessungsgrenze für Durchflusswert und Druck
DRUCK = 3
FLOW = 8

# TODO: Grenzwerte für Crack und Reseat
CRACKMAX = 2.2
CRACKMIN = 1.8
RESEATMIN = 1.6

# TODO: Name der Ergebnisdatei im .md-Format
# TODO: Bitte Beachten: DIe Ergebnisdatei manuell löschen! Dieses Script hängt immer nur an die aktuelle Datei an.
ERGEBNIS = "Ergebnis.md"

# -----PROGRAMM-----#
# For-Schleife wird für jede Datei im Verzeichnis 'USB' ausgeführt
for root, dirs, files in os.walk(USB):
    for FILE in files:
        if FILE.endswith(".csv"):
            # FILE ist tabulator getrennte csv-Datei
            data = pd.read_csv(FILE, delimiter="\t", error_bad_lines=False)

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
            TkService.showResultsInGrid(testData, reds, metaData)
