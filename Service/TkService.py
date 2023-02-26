import tkinter
from tkinter import messagebox
import tkinter as Tk

import numpy as np
import pandas as pd


def showNotification(errors):
    if len(errors) == 0:

        messagebox.showinfo("KEIN FEHLER", "Es wurden keine Fehler in den Messungen gefunden")

    else:
        messagebox.showwarning("FEHLER IN DEN MESSUNGEN",
                               "Es wurden Fehler in den Messungen gefunden. Öffne die Datei result.md um anzuzeigen")


def showResultsInGrid(testData, errors):
    root = Tk.Tk()
    root.winfo_toplevel().title("Messdaten von Verzeichnis")
    root.canvas = Tk.Canvas(root, width=500, height=500, borderwidth=1, highlightthickness=0)
    root.canvas.pack(side="top", fill="both", expand="true")
    numRows, numCols = testData.shape

    for row in range(numRows):
        for col in range(numCols):
            cellValue = testData.iloc[row, col]
            color = "black" if not errors[row, col] else "red"
            root.canvas.create_text(col * 100 + 50, row * 50 + 25, text=str(cellValue), fill=color)

    root.mainloop()
