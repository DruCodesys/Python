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
import os

#Dateipfad des USB-Sticks angeben. Für Entwicklungszwecke zunächst vom Root-Verzeichnis aus.
FILE = "../223061_LS1230093_1.csv"

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
operator = data['Crack_Pressure_Cycle1'][0]
order = data['Crack_Pressure_Cycle2'][0]
delivery = data['Crack_Pressure_Cycle3'][0]
delPos = data['Crack_Pressure_Cycle4'][0]
R1 = data['Reseat_Pressure_Cycle1']
header = ~R1.isna()

data = data[header]
Flow = data['Flow']
FP = data['Flow_Pressure']
SN = data['S/N']
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

figure, ax = plt.subplots(2,1,sharey=False)
ax[0].plot(SN, C1, 'x')
ax[0].plot(SN, R1, 'o')
ax[0].plot(SN, C2, 'x')
ax[0].plot(SN, R2, 'o')
ax[0].plot(SN, C3, 'x')
ax[0].plot(SN, R3, 'o')
ax[0].plot(SN, C4, 'x')
ax[0].plot(SN, R4, 'o')
ax[0].plot(SN, C5, 'x')
ax[0].plot(SN, R5, 'o')
ax[0].plot(SN, C6, 'x')
ax[0].plot(SN, R6, 'o')
ax[0].plot(SN, C7, 'x')
ax[0].plot(SN, R7, 'o')
ax[0].plot(SN, 2.2*np.ones(len(SN)), color= 'red')
ax[0].plot(SN, 1.8*np.ones(len(SN)), color= 'red')
ax[0].plot(SN, 1.6*np.ones(len(SN)), color= 'red')

ax[1].plot(SN, Flow.to_numpy(dtype='double'), 'x')
ax[1].plot(SN, FP.to_numpy(dtype='double'), 'o')
ax[1].plot(SN, 3*np.ones(len(SN)), color = 'red', linewidth=0.5)
ax[1].plot(SN, 8*np.ones(len(SN)), color = 'red', linewidth=0.5)
ax[0].legend(['C1', 'C2', 'C3','C4', 'C5', 'C6','C7', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'max. Crack', 'min. Crack', 'min. Reseat' ])
ax[1].legend(['Flow in m^3/h', "Druck in bar"])
plt.show()
