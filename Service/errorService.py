

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
                    errors.append("Fehler bei Ventil No.: " + str(SN[i]) + "Crack-Limit überschritten"+ "in Zyklus" + str(cycles.index(cycle) + 1))
                    errorIndex.append(['crack-Maximum', i])
        if valCrackMin[cycle].any():
            for i, element in enumerate(valCrackMax[cycle]):
                if element:
                    errors.append("Fehler bei Ventil No.: " + str(SN[i]) + "Crack-Limit unterschritten"+ "in Zyklus" + str(cycles.index(cycle) + 1))
                    errorIndex.append(['Crack-Minimum', i])
        if valReseatMin[cycle].any():
            for i, element in enumerate(valReseatMin[cycle]):
                if element:
                    errors.append("Fehler bei Ventil No.: " + str(SN[i]) + "Reseat-Limit unterschritten"+ "in Zyklus" + str(cycles.index(cycle) + 1))
                    errorIndex.append(['Reseat-Minimum', i])
        if val[cycle].any():
            for i, element in enumerate(val[cycle]):
                if element:
                    errors.append("Fehler bei Ventil No.: " + str(SN[i]) + " in Zyklus" + str(cycles.index(cycle) + 1)+": Reseat-Pressure > Crack-Pressure")
                    errorIndex.append([cycle, i])

    return errors, errorIndex