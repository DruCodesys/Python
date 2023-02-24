from tkinter import messagebox
import tkinter as Tk
def showNotification(errors):
    if len(errors) == 0:

        messagebox.showinfo("KEIN FEHLER", "Es wurden keine Fehler in den Messungen gefunden")

    else:
        messagebox.showwarning("FEHLER IN DEN MESSUNGEN",
                               "Es wurden Fehler in den Messungen gefunden. Öffne die Datei result.md um anzuzeigen")


def showResultsInGrid(testData, errors, index):
    root = Tk.Tk()
