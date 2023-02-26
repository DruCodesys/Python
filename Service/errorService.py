import numpy as np
import pandas as pd


def createErrors(val, valFlow, valFlowPressure, valCrackMax, valCrackMin, valReseatMin, SN):
    # Initialisiere Fehler-Array und schreibe die Fehler und Fehlerindizes in die Arrays
    errors = []
    errorIndex = []
    cycles = ["Cycle0", "Cycle1", "Cycle2", "Cycle3", "Cycle4", "Cycle5", "Cycle6"]
    if valFlowPressure.any():
        for i, element in enumerate(valFlowPressure):
            if element:
                errors.append("Fehler bei Ventil No.: " + str(SN[i]) + " im Flow-Druck")
                errorIndex.append(['FP', i])
    if valFlow.any():
        for i, element in enumerate(valFlow):
            if element:
                errors.append("Fehler bei Ventil No.: " + str(SN[i]) + " im Flow")
                errorIndex.append(['Flow', i])
    for cycle in cycles:
        if valCrackMax[cycle].any():
            for i, element in enumerate(valCrackMax[cycle]):
                if element:
                    errors.append(
                        "Fehler bei Ventil No.: " + str(SN[i]) + "Crack-Limit überschritten" + "in Zyklus" + str(
                            cycles.index(cycle) + 1))
                    errorIndex.append(['crack-Maximum', i])
        if valCrackMin[cycle].any():
            for i, element in enumerate(valCrackMax[cycle]):
                if element:
                    errors.append(
                        "Fehler bei Ventil No.: " + str(SN[i]) + "Crack-Limit unterschritten" + "in Zyklus" + str(
                            cycles.index(cycle) + 1))
                    errorIndex.append(['Crack-Minimum', i])
        if valReseatMin[cycle].any():
            for i, element in enumerate(valReseatMin[cycle]):
                if element:
                    errors.append(
                        "Fehler bei Ventil No.: " + str(SN[i]) + "Reseat-Limit unterschritten" + "in Zyklus" + str(
                            cycles.index(cycle) + 1))
                    errorIndex.append(['Reseat-Minimum', i])
        if val[cycle].any():
            for i, element in enumerate(val[cycle]):
                if element:
                    errors.append("Fehler bei Ventil No.: " + str(SN[i]) + " in Zyklus" + str(
                        cycles.index(cycle) + 1) + ": Reseat-Pressure > Crack-Pressure")
                    errorIndex.append([cycle, i])

    return errors, errorIndex


def setReds(value, errors, y, x):
    errors[x][y] = value
    if value:
        errors[y][0] = True
    return errors
def createErrorsBySN(val: pd.DataFrame, valFlow: pd.DataFrame, valFlowPressure: pd.DataFrame, valCrackMax: pd.DataFrame,
                     valCrackMin: pd.DataFrame, valReseatMin: pd.DataFrame, SN: pd.DataFrame):
    errors = []
    reds = np.zeros((valCrackMax.shape[0], valCrackMax.shape[1] + 1 + valReseatMin.shape[1] ), dtype=bool)
    cycles = ["Cycle0", "Cycle1", "Cycle2", "Cycle3", "Cycle4", "Cycle5", "Cycle6"]
    for i, element in enumerate(SN):
        if valFlow[i]:
            errors.append("Fehler bei Ventil No.: " + str(element) + " im Flow-Druck")
            reds = setReds(True, reds, 1, i)
        if valFlowPressure[i]:
            errors.append("Fehler bei Ventil No.: " + str(element) + " im Flow-Druck")
            reds = setReds(True, reds, 2, i)
        for j, cycle in enumerate(cycles):
            if valCrackMax[cycle][i]:
                errors.append(
                    "Fehler bei Ventil No.: " + str(element) + "Crack-Limit überschritten" + "in Zyklus" + str(
                        j + 1))
                reds = setReds(True, reds, cycles.index(cycle)+3, i)
            if valCrackMin[cycle][i]:
                errors.append(
                    "Fehler bei Ventil No.: " + str(element) + "Crack-Limit unterschritten" + "in Zyklus" + str(
                        j + 1))
                reds = setReds(True, reds, cycles.index(cycle)+3, i)
            if valReseatMin[cycle][i]:
                errors.append(
                    "Fehler bei Ventil No.: " + str(element) + "Reseat-Limit unterschritten" + "in Zyklus" + str(
                        j + 1))
                reds = setReds(True, reds, cycles.index(cycle)+1 + valCrackMax.shape[1], i)
            if val[cycle][i]:
                errors.append("Fehler bei Ventil No.: " + str(element) + " in Zyklus" + str(
                    j + 1) + ": Reseat-Pressure > Crack-Pressure")
                reds = setReds(True, reds, cycles.index(cycle) + valCrackMax.shape[1]+2, i)
                reds = setReds(True, reds, cycles.index(cycle) + 3, i)

    return errors, reds
