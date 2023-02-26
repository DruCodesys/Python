import tkinter
from tkinter import messagebox

import tkinter as Tk
import tkinter.font as font

import numpy as np
import pandas as pd

def rgbaToHex(rgba):
    r, g, b = rgba
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def showNotification(errors):
    if len(errors) == 0:

        messagebox.showinfo("KEIN FEHLER", "Es wurden keine Fehler in den Messungen gefunden")

    else:
        messagebox.showwarning("FEHLER IN DEN MESSUNGEN",
                               "Es wurden Fehler in den Messungen gefunden. Öffne die Datei result.md um anzuzeigen")


import tkinter as Tk


def showResultsInGrid(testData, errors, metaData):
    root = Tk.Tk()
    root.winfo_toplevel().title("Messdaten von Verzeichnis")

    # Calculate total width and height of data
    numRows, numCols = testData.shape
    totalWidth = numCols * 100
    totalHeight = numRows * 50

    # Create Label with metadata
    root.Label = Tk.Label(root, text= f"Datei: {metaData['origin'][0]}, Datum: {metaData['date'][0]}, Prüfer: {metaData['operator'][0]}")
    root.Label.pack(side="top", fill="both", expand="true")
    # Create canvas and frame
    root.canvas = Tk.Canvas(root, width=500, height=500, borderwidth=1, highlightthickness=0)
    root.canvas.pack(side="top", fill="both", expand="true")
    root.frame = Tk.Frame(root.canvas, width=totalWidth, height=totalHeight)
    root.frame.pack(side="top", fill="both", expand="true")

    # Add horizontal scrollbar
    hbar = Tk.Scrollbar(root, orient="horizontal", command=root.canvas.xview)
    hbar.pack(side="bottom", fill="x")
    root.canvas.configure(xscrollcommand=hbar.set)

    boldFont = font.Font(weight="bold")

    colTitles = ["S/N", "Flow", "FlowPress", "Crack#1", "Crack#2", "Crack#3", "Crack#4", "Crack#5", "Crack#6", "Crack#7", "Reseat#1", "Reseat#2", "Reseat#3", "Reseat#4", "Reseat#5", "Reseat#6", "Reseat#7"]
    # Add data to frame
    for row in range(numRows+1):
        for col in range(numCols):
            if row ==0:
                cellValue = colTitles[col]
            else:
                cellValue = testData.iloc[row-1, col]
            color = "black" if not errors[row-1, col] else "red"
            cellLabel = Tk.Label(root.frame, text=str(cellValue), fg=color)
            if col == 0 or errors[row-1, col] or row == 0:
                cellLabel['font'] = boldFont
            cellLabel.grid(row=row, column=col, padx=5, pady=5, sticky='news')

    # Create lines
    for i in range(numRows + 1):
        x1 = 0
        x2 = totalWidth
        y = i * 50
        root.canvas.create_line(x1, y, x2, y, fill='grey')

    for i in range(numCols + 1):
        y1 = 0
        y2 = totalHeight
        x = i * 100
        root.canvas.create_line(x, y1, x, y2, fill='grey')

    # Configure canvas to scroll frame
    root.frame.update_idletasks()
    root.canvas.config(scrollregion=root.canvas.bbox("all"))

    # Add close button
    closeButton = Tk.Button(root, text="Schließen und Nächste Daten zeigen", command=root.destroy, width=0, height=0,
                            bg=rgbaToHex((50, 50, 255)), fg=rgbaToHex((0, 0, 0)))

    # The width and height parameters control the width and height of the button in pixels.
    buttonFont = font.Font(family = "Helvetica", weight="bold")
    closeButton.pack(side="bottom", pady=10)
    closeButton['font'] = buttonFont

    root.focus_force()
    root.mainloop()




