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


def setReds(value, reds, row, col):
    reds[row][col] = value
    if value:
        reds[row][0] = True
    return reds
def createErrorsBySN(val: pd.DataFrame, valFlow: pd.DataFrame, valFlowPressure: pd.DataFrame, valCrackMax: pd.DataFrame,
                     valCrackMin: pd.DataFrame, valReseatMin: pd.DataFrame, SN: pd.DataFrame):
    errors = []
    reds = np.zeros((valCrackMax.shape[0], valCrackMax.shape[1] + 1 + valReseatMin.shape[1] ), dtype=bool)
    cycles = ["Cycle0", "Cycle1", "Cycle2", "Cycle3", "Cycle4", "Cycle5", "Cycle6"]
    for i, element in enumerate(SN):
        if valFlow[i]:
            errors.append("Fehler bei Ventil No.: " + str(element) + " im Flow-Druck")
            reds = setReds(True, reds, i, 1)
        if valFlowPressure[i]:
            errors.append("Fehler bei Ventil No.: " + str(element) + " im Flow")
            reds = setReds(True, reds, i, 2)
        for j, cycle in enumerate(cycles):
            if valCrackMax[cycle][i]:
                errors.append(
                    "Fehler bei Ventil No.: " + str(element) + "Crack-Limit überschritten" + "in Zyklus" + str(
                        j + 1))
                reds = setReds(True, reds, i, cycles.index(cycle)+3)
            if valCrackMin[cycle][i]:
                errors.append(
                    "Fehler bei Ventil No.: " + str(element) + "Crack-Limit unterschritten" + "in Zyklus" + str(
                        j + 1))
                reds = setReds(True, reds, i, cycles.index(cycle)+3)
            if valReseatMin[cycle][i]:
                errors.append(
                    "Fehler bei Ventil No.: " + str(element) + "Reseat-Limit unterschritten" + "in Zyklus" + str(
                        j + 1))
                reds = setReds(True, reds, i, cycles.index(cycle)+1 + valCrackMax.shape[1])
            if val[cycle][i]:
                errors.append("Fehler bei Ventil No.: " + str(element) + " in Zyklus" + str(
                    j + 1) + ": Reseat-Pressure > Crack-Pressure")
                reds = setReds(True, reds, i, cycles.index(cycle) + valCrackMax.shape[1]+2)
                reds = setReds(True, reds, i, cycles.index(cycle) + 3)

    return errors, reds
