# -*- coding: utf-8 -*-
"""
Created on Tue May  4 10:00:40 2021

@author: Anthony Araujo Fernandez
"""

import tkinter as tk 
from tkinter import filedialog
from tkinter import *
import os

ventana = Tk()
ventana.title("Hass Peru")
ventana.geometry('300x300')
ventana.configure(bg='gray26')

image = tk.PhotoImage(file="logo_HASS_Horizontal.gif")
image = image.subsample(1,1)
label = tk.Label(image = image)
label.place(x=20, y=10) 


def abrir_archivo():
    archivo_abierto=filedialog.askopenfilename(initialdir = "/",
                title = "Seleccione archivo",filetypes = (("pdf files","*.pdf"),
                ("all files","*.*")))
    print(archivo_abierto)

Button(text="Abrir archivo",bg="pale green",command=abrir_archivo).place(x=100,y=200)

ventana.mainloop()