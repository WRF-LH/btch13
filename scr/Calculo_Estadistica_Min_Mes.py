#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 14:00:49 2018

@author: andres

Este script toma las imagenes de folder - calcula el minimo de cada pixel en el dia - devuelve un nuevo archivo .nc
"""

import numpy.ma as ma
import numpy as np
import pylab as plt
from netCDF4 import Dataset
from os import listdir
from os.path import isfile, join
#from cpt_convert import loadCPT # Import the CPT convert function
from matplotlib.colors import LinearSegmentedColormap
import shutil
import os


mes='201801'#---------------------------------------------------->>>> cambia dia a dia

folder = '/home/alighezzolo/BTCH13/OUTPUTS/NC/'+mes+'/minima/'

imagenes_plots = [f for f in listdir(folder) if isfile(join(folder, f)) and f.endswith('.nc')]
imagenes_plots.sort()

longitud=len(imagenes_plots)
print('número de imagenes =',longitud)

####Abre la primera imagen - la usa como minimo inicial
IMG_GOES16_0 = Dataset(folder+imagenes_plots[0])
minimo = IMG_GOES16_0.variables['CMI'][:]

output2=folder+'Minima_'+mes+'.nc'
shutil.copy(folder+imagenes_plots[0],output2)#Copia y renombre el .nc

######Calculo del minimo


for i in range(1,longitud):
    IMG_GOES16_0 = Dataset(folder+imagenes_plots[i])
    Valores_TB_0 = IMG_GOES16_0.variables['min'][:]
    minimo=np.minimum(minimo,Valores_TB_0)
    
    print(i)
print(minimo[4200,3800])


####################################Escritura en NETCDF agregando una nueva variable llamada min

filename=folder+'Minima_'+mes+'.nc' ####El archivo a crear no debe tener la variable escrita

ncfile = Dataset(filename,'r+')
data=ncfile.createVariable('mes_min',ncfile.variables['CMI'].dtype.char, ('x','y'))
data[:]=minimo
ncfile.close()

