import numpy as np
import pandas as pd


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
            errors.append("Fehler bei Ventil No.: " + str(element) + " im Flow")
            reds = setReds(True, reds, i, 1)
        if valFlowPressure[i]:
            errors.append("Fehler bei Ventil No.: " + str(element) + " im Flow-Druck")
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
