import pandas as pd


def evaluateCrackReseat(testData):
    # Berechne die Felder in denen Der Reseat-Pressure größer oder gleich dem Crack-Pressure ist
    val = pd.DataFrame()
    val["Cycle0"] = testData['R1'] >= testData['C1']
    val["Cycle1"] = testData['R2'] >= testData['C2']
    val["Cycle2"] = testData['R3'] >= testData['C3']
    val["Cycle3"] = testData['R4'] >= testData['C4']
    val["Cycle4"] = testData['R5'] >= testData['C5']
    val["Cycle5"] = testData['R6'] >= testData['C6']
    val["Cycle6"] = testData['R7'] >= testData['C7']
    return val


def evaluateFlow(testData, FLOW):
    valFlow = pd.DataFrame()
    valFlow = testData['Flow'] < FLOW
    return valFlow


def evaluateFlowPressure(testData, DRUCK):
    valFlowPressure = pd.DataFrame()
    valFlowPressure = testData['FP'] > DRUCK
    return valFlowPressure
