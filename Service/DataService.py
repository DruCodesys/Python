import pandas as pd


def DataService(data):
    # Header sind Zeilen 0, 8, 17 --> Unregelmäßig
    # Metadaten sind in den Zeilen 1, 9, 18 --> Unregelmäßig
    SN = data['S/N']

    # entferne die Kopfzeilen
    header = SN != 'S/N'
    data = data[header]

    # lese meta-daten aus
    date = data['S/N'][0]
    origin = data['pos'][0]
    operator = data['Crack_Pressure_Cycle1'][0]
    order = data['Crack_Pressure_Cycle2'][0]
    delivery = data['Crack_Pressure_Cycle3'][0]
    delPos = data['Crack_Pressure_Cycle4'][0]

    metaData = metaData = pd.DataFrame({'date': [date], 'origin': [origin], 'operator': [operator], 'order': [order], 'delivery': [delivery], 'delPos': [delPos]})


    # entferne die Zeilen mit Metadaten
    R1 = data['Reseat_Pressure_Cycle1']
    header = ~R1.isna()
    data = data[header]

    # Konvertiere die Datentypen string -> double/int in numpy - Array
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

    # Erstelle Datenframe aus numpy-Spalten
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
    return testData, SN, metaData

def writeData(FILE, metaData, errors, testData):
    with open(FILE, 'a') as file:
        file.write('\n______\n')
        file.write(f" ## Messergebnise aus {metaData['origin']}\n\n")
        file.write('\n')
        file.write(
            f"Aus Datei: {metaData['origin']} Prüfer: {metaData['operator']} Datum: {metaData['date']} Auftrag: {metaData['order']} Lieferschein: {metaData['delivery']} Lieferscheinposition: {metaData['delPos']}")
        file.write('\n\n')
        file.close()
    testData.to_markdown(FILE, mode='a')
    with open(FILE, 'a') as file:
        file.write("\n")
        for element in errors:
            file.write("\n" + element + "\n")
        file.write("\n")
        file.close()
