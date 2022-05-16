# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 09:17:38 2021

@author: Anthony Araujo Fernandez 
"""

import os 
from pdf2image import convert_from_path
 
os.chdir(r'C:\Users\Usuario\Desktop\PROYECTO PRUEBA\PDF')
images = convert_from_path('C:\Users\Usuario\Desktop\PROYECTO PRUEBA\PDF\prueba.pdf')

os.chdir(r'C:\Users\Usuario\Desktop\PROYECTO PRUEBA\IMG')
for i in range(len(images)):
    images[i].save('page'+ str(i) +'.jpg', 'JPEG')
    

    

