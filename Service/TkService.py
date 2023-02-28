from tkinter import messagebox
import tkinter.font as font
import pandas as pd
import numpy as np

import sys
import tkinter as tk


def rgbaToHex(rgba):
    r, g, b = rgba
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def _on_mousewheel(event):
    canvas.yview_scroll(-1*(event.delta/120), "units")

def showNotification(errors):
    if len(errors) == 0:

        messagebox.showinfo("KEIN FEHLER", "Es wurden keine Fehler in den Messungen gefunden")

    else:
        messagebox.showwarning("FEHLER IN DEN MESSUNGEN",
                               "Es wurden Fehler in den Messungen gefunden. Öffne die Datei result.md um anzuzeigen")


def showResultsInGrid(testData, errors, metaData, errorlist):
    # Calculate total width and height of data
    numRows, numCols = testData.shape
    cellWidth = 80
    cellHeight = 30
    xFactor = 1
    xOffset = 0.5 * cellWidth
    yOffset = 15
    totalWidth = numCols * 80
    totalHeight = numRows * 30

    root = tk.Tk()
    root.winfo_toplevel().title("Messdaten von Verzeichnis")

    # Create Label with metadata
    root.Label = tk.Label(root,
                          text=f"Datei: {metaData['origin'][0]}, Datum: {metaData['date'][0]}, "
                               f"Prüfer: {metaData['operator'][0]}")
    root.Label.pack(side="top", fill="both", expand=0)

    # Create canvas and frame
    root.canvas = tk.Canvas(root, width=500, height=500, borderwidth=1, highlightthickness=0)
    root.canvas.pack(side="top", fill="both", expand=1)
    #root.canvas.bind_all("<MouseWheel>", _on_mousewheel)
    # Add vertical scrollbar
    vbar = tk.Scrollbar(root.canvas, orient="vertical", command=root.canvas.yview)
    vbar.pack(side="right", fill="y")
    root.canvas.configure(yscrollcommand=vbar.set)

    # Add horizontal scrollbar
    hbar = tk.Scrollbar(root, orient="horizontal", command=root.canvas.xview)
    hbar.pack(side="bottom", fill="x")
    root.canvas.configure(xscrollcommand=hbar.set)

    boldFont = font.Font(weight="bold", size=8)

    colTitles = ["S/N", "Flow", "FP", "Crack#1", "Crack#2", "Crack#3", "Crack#4", "Crack#5", "Crack#6",
                 "Crack#7", "Reseat#1", "Reseat#2", "Reseat#3", "Reseat#4", "Reseat#5", "Reseat#6", "Reseat#7"]

    # Add data to the frame

    for row in range(numRows + 1):
        for col in range(numCols):
            if row == 0:
                cellValue = colTitles[col]
            else:
                cellValue = testData.iloc[row - 1, col]
            color = "black" if not errors[row - 1, col] else "red"
            if col == 0:
                setfont = boldFont
            else:
                setfont = None
            root.canvas.create_text(
                col * cellWidth * xFactor + xOffset,
                row * cellHeight + yOffset,
                text=cellValue, anchor='center',
                width=cellWidth,
                fill=color,
                font=setfont
            )

    # Create lines
    for i in range(numRows + 2):  # horizontal lines
        x1 = 0
        x2 = totalWidth
        y = i * cellHeight
        root.canvas.create_line(x1, y, x2, y, fill='grey')

    for i in range(numCols + 1):  # vertical lines
        y1 = 0
        y2 = totalHeight + cellHeight
        x = i * (cellWidth)
        root.canvas.create_line(x, y1, x, y2, fill='grey')

    # Add errorlist
    for element in errorlist:
        root.label = tk.Label(root, text=element)
        root.label.pack(side='top', fill='x', expand=0)

    # Add close button
    closeButton = tk.Button(root, text="Schließen und Nächste Daten zeigen", command=root.destroy, width=0, height=0,
                            bg=rgbaToHex((50, 50, 255)), fg=rgbaToHex((0, 0, 0)))

    # The width and height parameters control the width and height of the button in pixels.
    buttonFont = font.Font(family="Helvetica", weight="bold")
    closeButton.pack(side="bottom", pady=10)
    closeButton['font'] = buttonFont

    # Configure canvas to scroll frame
    root.canvas.update_idletasks()
    root.canvas.config(scrollregion=root.canvas.bbox("all"))

    root.focus_force()
    root.mainloop()
