#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 17:24:06 2019

@author: andres
"""

import numpy.ma as ma
import numpy as np
import pylab as plt
from netCDF4 import Dataset
from os import listdir
from os.path import isfile, join
from cpt_convert import loadCPT # Import the CPT convert function
import shutil
import os
import sys
#dia='2018002'#---------------------------------------------------->>>> cambia dia a dia
dia=sys.argv[1]+sys.argv[2]

dire_out='/home/alighezzolo/BTCH13/OUTPUTS/NC/'+dia+'/frecuencia_diaria/'
os.makedirs(dire_out)

umbral=210#183.15#-90
folder = '/home/alighezzolo/BTCH13/DATA/'+dia+'/'
#output = '/media/andres/Elements/GOES16/BTCH13/OUTPUTS/'+dia+'/nc/frecuencia_diaria/'



imagenes_plots = [f for f in listdir(folder) if isfile(join(folder, f)) and f.endswith('.nc')]
imagenes_plots.sort()

longitud=len(imagenes_plots)
print('número de imagenes =',longitud)


##################################copiado de .nc template


####COPIAR un .nc a la carpeta de OUTPUTS y renombrarla para que sirva de template en la creacion del nuevo .nc

#day = (folder+imagenes_plots[0])[46:53]#toma el dia desde el nombre de la imagen
output2='/home/alighezzolo/BTCH13/OUTPUTS/NC/'+dia+'/frecuencia_diaria/frecuencia_d_'+dia+"_"+str(umbral)+"K_FD.nc"
shutil.copy(folder+imagenes_plots[0],output2)#Copia y renombre el .nc



##################################

Maux_0=np.zeros((5424,5424))

Maux_1=np.zeros((5424,5424))

#Maux_0=Maux_0+9999




for i in range(0,longitud):
    IMG_GOES16_0 = Dataset(folder+imagenes_plots[i])
    Valores_TB_0 = IMG_GOES16_0.variables['CMI'][:]
    
    Maux_0=Maux_0+9999
    Maux_0[Valores_TB_0<umbral]=Valores_TB_0[Valores_TB_0<umbral]
    Maux_0[Maux_0 < umbral]=1
    Maux_0[Maux_0 > 9998]=0
    Maux_1=Maux_1+Maux_0
    #print (i)
    print(Maux_1[4200,3800])
    #print(Maux_0[4200,3800].sum())
    
fig = plt.figure()
imagen_REF = plt.imshow(Maux_1, origin='upper', vmin=0, vmax=48, cmap='jet')
plt.title('Numero de eventos - Umbral:'+str(umbral)+'K - Dia:'+str(dia))
plt.ylabel('coordenadas Y')
plt.xlabel('coordenadas X')
cb = fig.colorbar(imagen_REF, orientation='vertical')
#cb.set_ticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6 ,0.7, 0.8, 0.9, 1])
cb.set_label('Eventos diarios por pixel')

#lt.savefig(dire_out+'frecuencia_d_'+day+'_'+str(umbral)+'K_FD.png',dpi=300)


##########################################################NETCDF
filename='/home/alighezzolo/BTCH13/OUTPUTS/NC/'+dia+'/frecuencia_diaria/frecuencia_d_'+dia+"_"+str(umbral)+"K_FD.nc"
 ####El archivo a crear no debe tener la variable escrita

ncfile = Dataset(filename,'r+')
data=ncfile.createVariable('frec',ncfile.variables['CMI'].dtype.char, ('x','y'))
data[:]=Maux_1
ncfile.close()
