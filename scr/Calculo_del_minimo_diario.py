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
import sys

#dia='2018002'#---------------------------------------------------->>>> cambia dia a dia
dia=sys.argv[1]+sys.argv[2]

dire_out='/home/alighezzolo/BTCH13/OUTPUTS/NC/'+dia+'/minimo_diario/'
os.makedirs(dire_out)

folder = '/home/alighezzolo/BTCH13/DATA/'+dia+'/'


imagenes_plots = [f for f in listdir(folder) if isfile(join(folder, f)) and f.endswith('.nc')]
imagenes_plots.sort()

longitud=len(imagenes_plots)
print('número de imagenes =',longitud)

####Abre la primera imagen - la usa como minimo inicial
IMG_GOES16_0 = Dataset(folder+imagenes_plots[0])
minimo = IMG_GOES16_0.variables['CMI'][:]

####COPIAR un .nc a la carpeta de OUTPUTS y renombrarla para que sirva de template en la creacion del nuevo .nc

#day = (folder+imagenes_plots[0])[46:53]#toma el dia desde el nombre de la imagen
output='/home/alighezzolo/BTCH13/OUTPUTS/NC/'+dia+'/minimo_diario/minimo_d_'+dia+'.nc'
shutil.copy(folder+imagenes_plots[0],output)#Copia y renombre el .nc




######Calculo del minimo


for i in range(1,longitud):
    IMG_GOES16_0 = Dataset(folder+imagenes_plots[i])
    Valores_TB_0 = IMG_GOES16_0.variables['CMI'][:]
    minimo=np.minimum(minimo,Valores_TB_0)
    
    print(i)
print(minimo[4200,3800])

#np.save('minimo_20181228.npy',minimo.data)
#
#minimo_20181228=np.load('minimo_20181228.npy')
#cpt=loadCPT('/media/andres/Elements/GOES16/cpt/IR4AVHRR6.cpt')
#cpt_convert = LinearSegmentedColormap('cpt', cpt)
#    
#fig = plt.figure()
#imagen_REF = plt.imshow(minimo_20181228-273.15, origin='upper', vmin=-90, vmax=50, cmap=cpt_convert)
#plt.title('Imagen de Temperatura de brillo - CH 13 micrones')
#plt.ylabel('coordenadas Y')
#plt.xlabel('coordenadas X')
#cb = fig.colorbar(imagen_REF, orientation='vertical')
##cb.set_ticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6 ,0.7, 0.8, 0.9, 1])
#cb.set_label('Temperatura de brillo')
#
#plt.savefig('/media/andres/Elements/GOES16/Estadistica/goya_20180630/plots/BT_CH_13_20181228.png',dpi=300)

####################################Escritura en NETCDF agregando una nueva variable llamada min

filename='/home/alighezzolo/BTCH13/OUTPUTS/NC/'+dia+'/minimo_diario/minimo_d_'+dia+'.nc' ####El archivo a crear no debe tener la variable escrita

ncfile = Dataset(filename,'r+')
data=ncfile.createVariable('min',ncfile.variables['CMI'].dtype.char, ('x','y'))
data[:]=minimo
ncfile.close()



