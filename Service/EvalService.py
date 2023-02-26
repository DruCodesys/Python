import pandas as pd


def evaluateCrackReseat(testData):
    # Berechne die Felder in denen Der Reseat-Pressure größer oder gleich dem Crack-Pressure ist
    val = pd.DataFrame()#
    val["SN"] = testData["SN"]
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
    valFlow["SN"] = testData["SN"]
    valFlow = testData['Flow'] < FLOW
    return valFlow


def evaluateFlowPressure(testData, DRUCK):
    valFlowPressure = pd.DataFrame()
    valFlowPressure["SN"] = testData["SN"]
    valFlowPressure = testData['FP'] > DRUCK
    return valFlowPressure


def evaluateCrackMax(testData, CRACKMAX):
    crackMax = pd.DataFrame()
    crackMax["SN"] = testData["SN"]
    crackMax["Cycle0"] = testData['C1'] > CRACKMAX
    crackMax["Cycle1"] = testData['C2'] > CRACKMAX
    crackMax["Cycle2"] = testData['C3'] > CRACKMAX
    crackMax["Cycle3"] = testData['C4'] > CRACKMAX
    crackMax["Cycle4"] = testData['C5'] > CRACKMAX
    crackMax["Cycle5"] = testData['C6'] > CRACKMAX
    crackMax["Cycle6"] = testData['C7'] > CRACKMAX
    return crackMax


def evaluateCrackMin(testData, CRACKMIN):
    crackMin = pd.DataFrame()
    crackMin["SN"] = testData["SN"]
    crackMin["Cycle0"] = testData['C1'] < CRACKMIN
    crackMin["Cycle1"] = testData['C2'] < CRACKMIN
    crackMin["Cycle2"] = testData['C3'] < CRACKMIN
    crackMin["Cycle3"] = testData['C4'] < CRACKMIN
    crackMin["Cycle4"] = testData['C5'] < CRACKMIN
    crackMin["Cycle5"] = testData['C6'] < CRACKMIN
    crackMin["Cycle6"] = testData['C7'] < CRACKMIN
    return crackMin


def evaluateReseatMin(testData, RESEATMIN):
    reseatMin = pd.DataFrame()
    reseatMin["SN"] = testData["SN"]
    reseatMin["Cycle0"] = testData['R1'] < RESEATMIN
    reseatMin["Cycle1"] = testData['R2'] < RESEATMIN
    reseatMin["Cycle2"] = testData['R3'] < RESEATMIN
    reseatMin["Cycle3"] = testData['R4'] < RESEATMIN
    reseatMin["Cycle4"] = testData['R5'] < RESEATMIN
    reseatMin["Cycle5"] = testData['R6'] < RESEATMIN
    reseatMin["Cycle6"] = testData['R7'] < RESEATMIN
    return reseatMin