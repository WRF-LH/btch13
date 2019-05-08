#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 15:17:23 2019

@author: andres
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:24:04 2019

@author: andres
"""

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

mes='201801'#---------------------------------------------------->>>> cambia dia a dia

folder = '/home/alighezzolo/BTCH13/OUTPUTS/NC/'+mes+'/'


imagenes_plots = [f for f in listdir(folder) if isfile(join(folder, f)) and f.endswith('.nc')]
imagenes_plots.sort()

longitud=len(imagenes_plots)
print('número de imagenes =',longitud)

##################################copiado de .nc template


####COPIAR un .nc a la carpeta de OUTPUTS y renombrarla para que sirva de template en la creacion del nuevo .nc

#day = (folder+imagenes_plots[0])[46:53]#toma el dia desde el nombre de la imagen
output2=folder+'Frecuencia_'+mes+'.nc'
shutil.copy(folder+imagenes_plots[0],output2)#Copia y renombre el .nc


Maux_0=np.zeros((5424,5424))

for i in range(0,longitud):
    IMG_GOES16_0 = Dataset(folder+imagenes_plots[i])
    Valores_TB_0 = IMG_GOES16_0.variables['frec'][:]
    
    Maux_0=Maux_0 + Valores_TB_0

      
    #print (Valores_TB_0[i].max)
    #print(Maux_0[4200,3800])
    #print(Maux_0[4200,3800].sum())
    
#fig = plt.figure()
#imagen_REF = plt.imshow(Valores_TB_0, origin='upper', vmin=0, vmax=3, cmap='jet')
#plt.title('Numero de eventos')
#plt.ylabel('coordenadas Y')
#plt.xlabel('coordenadas X')
#cb = fig.colorbar(imagen_REF, orientation='vertical')
#cb.set_ticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6 ,0.7, 0.8, 0.9, 1])
#cb.set_label('Eventos diarios por pixel')

#plt.savefig(folder+'Frecuencia_'+mes+'_FD.png',dpi=300)


    
    
    
    
filename=folder+'Frecuencia_'+mes+'.nc' ####El archivo a crear no debe tener la variable escrita

ncfile = Dataset(filename,'r+')
data=ncfile.createVariable('mes_frec',ncfile.variables['CMI'].dtype.char, ('x','y'))
data[:]=Maux_0
ncfile.close()
