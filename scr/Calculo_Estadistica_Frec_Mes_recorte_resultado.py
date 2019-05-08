#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 15:41:39 2019

@author: andres
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 13:36:44 2019

@author: andres
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 11:17:15 2019

@author: andres
"""

import numpy.ma as ma
import numpy as np
import pylab as plt
from netCDF4 import Dataset
from os import listdir
from os.path import isfile, join
from cpt_convert import loadCPT # Import the CPT convert function
from matplotlib.colors import LinearSegmentedColormap
from osgeo import osr,gdal
from mpl_toolkits.basemap import Basemap # Import the Basemap toolkit

mes='201801'#---------------------------------------------------->>>> cambia dia a dia
umbral=210#183.15#-90

folder = '/home/alighezzolo/BTCH13/OUTPUTS/NC/'+mes+'/'####al .nc de frecuencia


direcpt='/home/alighezzolo/BTCH13/CPT/'

dires='/home/alighezzolo/BTCH13/SHAPES/'

######################Carga y ordena imagenes

imagenes_plots = [f for f in listdir(folder) if isfile(join(folder, f)) and f.endswith(mes+'.nc')]
imagenes_plots.sort()

longitud=len(imagenes_plots)
print('número de imagenes =',longitud)


##########################################
#%% Lectura de Metadatos

#archiM=folder2+imagenes_plots[0][0:73]+'.txt'
archiM=folder+'/Frecuencia_'+mes+'.txt'
arch = open (archiM,'r')
lines=arch.readlines()
    
icanal=int(lines[3].split('#')[0])
cols=int(lines[5].split('#')[0])
rows=int(lines[6].split('#')[0])
t_0=float(lines[12].split('#')[0]) #####ver para que!
t_start=lines[13][14:33] # Fecha correspondiente a 0s     VER para que? 

#Parametros de proyeccion          
proj=lines[14].split('#')[0]
lat_0=lines[19].split('#')[0]
lon_0=lines[20].split('#')[0]
h=lines[21].split('#')[0]
a=lines[22].split('#')[0]
b=lines[23].split('#')[0]
f=1/float(lines[24].split('#')[0])

              #Parametross de calibracion         
offset=float(lines[25].split('#')[0]) #DN->L
scale=float(lines[26].split('#')[0])
                
arch.close
############################################

#########################genero matriz minima con la imagen inicial
VAR='mes_frec'

connectionInfo_0 = 'HDF5:\"' + folder+'Frecuencia_'+mes+'.nc' + '\"://'+VAR #####CAMBIAR ACA!!
        
minimo = gdal.Open(connectionInfo_0, gdal.GA_ReadOnly)

#######################
sourcePrj = osr.SpatialReference() # GOES-16 Spatial Reference System

sourcePrj.ImportFromProj4('+proj=geos +h='+h+' +a='+a+' +b='+b+' +f='+str(f)
                              +'lat_0='+lat_0+' +lon_0='+lon_0+' +sweep=x +no_defs')


# Lat/lon WSG84 Spatial Reference System
targetPrj = osr.SpatialReference()
targetPrj.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')



    # Setup projection and geo-transformation
# GOES-16 Extent (satellite projection) [llx, lly, urx, ury]
GOES16_EXTENT = [-5434894.885056, -5434894.885056, 5434894.885056, 5434894.885056]


def getGeoT(extent, nlines, ncols):
    # Compute resolution based on data dimension
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3] , 0, -resy]

minimo.SetProjection(sourcePrj.ExportToWkt())
minimo.SetGeoTransform(getGeoT(GOES16_EXTENT, minimo.RasterYSize, minimo.RasterXSize))


###################
extent = [-76, -56, -51, -20]
# Define KM_PER_DEGREE
KM_PER_DEGREE = 111.32
resolution=1.
    # Compute grid dimension
sizex = int(((extent[2] - extent[0]) * KM_PER_DEGREE) / resolution)
sizey = int(((extent[3] - extent[1]) * KM_PER_DEGREE) / resolution)
        
    # Get memory driver
memDriver = gdal.GetDriverByName('MEM')
       
    # Create grid
grid_minimo = memDriver.Create('grid', sizex, sizey, 1, gdal.GDT_Float32)



    # Setup projection and geo-transformation
grid_minimo.SetProjection(targetPrj.ExportToWkt())
grid_minimo.SetGeoTransform(getGeoT(extent, grid_minimo.RasterYSize, grid_minimo.RasterXSize))

#resultado=np.load('/media/andres/Elements/GOES16/Estadistica/minimo_20181228.npy')

gdal.ReprojectImage(minimo, grid_minimo, sourcePrj.ExportToWkt(), targetPrj.ExportToWkt(), gdal.GRA_NearestNeighbour, options=['NUM_THREADS=ALL_CPUS']) 

    # Read grid data
array_01 = grid_minimo.ReadAsArray()


    # Mask fill values (i.e. invalid values)
np.ma.masked_where(array_01, array_01 == -1, False)

grid_minimo.GetRasterBand(1).SetNoDataValue(-1)
grid_minimo.GetRasterBand(1).WriteArray(array_01)

#resultado=np.load('/media/andres/Elements/GOES16/Estadistica/minimo_20181228.npy')

array_01 = array_01*0.25 #* scale + offset -------------------------------------->>>>>>>>>>>>>escala!!!!!!

print(np.max(array_01))
##########################################creacion del mapa

fig= plt.figure(num=1,clear='True')
fig= plt.figure(num=1,figsize=[20,16],dpi=300,frameon='False') #frameon es para NO desplegar la figura 

bmap = Basemap(resolution='h',llcrnrlon=extent[0], llcrnrlat=extent[1], 
                   urcrnrlon=extent[2], urcrnrlat=extent[3], epsg=4326)#4326 es WGS84 (LatLOn)


bmap.imshow(array_01,origin='upper')

bmap.readshapefile(dires+'008_limites_provinciales_LL','008_limites_provinciales_LL',linewidth=0.5,color='black')
bmap.readshapefile(dires+'DEPARTAMENTOS_linea','DEPARTAMENTOS_linea',linewidth=0.2,color='black')#bmap.readshapefile(dires3+'Límites_internacionales','Límites_internacionales',linewidth=0.3,color='w')


bmap.drawparallels(np.arange(-90.0, 90.0, 3.), linewidth=0.3, dashes=[4, 4], 
                       color='white', labels=[True,True,False,False], fmt='%g', labelstyle="+/-", xoffset=0.10, yoffset=-1.00, size=5)
bmap.drawmeridians(np.arange(0.0, 360.0, 3.), linewidth=0.3, dashes=[4, 4], 
                       color='white', labels=[False,False,True,False], fmt='%g', labelstyle="+/-", xoffset=-0.80, yoffset=0.20, size=5)
 
    
# Converts a CPT file to be used in Python
    #cptfile = "crisp_ice.cpt"
cptfile='precip3_16lev.cpt'

cpt = loadCPT(direcpt+cptfile)
    
    # Makes a linear interpolation
cpt_convert = LinearSegmentedColormap('cpt', cpt)



img_plot=bmap.imshow(array_01, origin='upper', cmap=cpt_convert, vmin=0, vmax=65)

# Insert the colorbar at the right
cb = bmap.colorbar(location='bottom', size = '2%', pad = '1%')
cb.outline.set_visible(True) # Remove the colorbar outline
cb.ax.tick_params(width = 0) # Remove the colorbar ticks
cb.ax.xaxis.set_tick_params(pad=-2) # Put the colobar labels inside the colorbar
cb.ax.tick_params(axis='x', colors='black', labelsize=6) # Change the color and size of the colorbar labels
Unit = "Horas bajo umbral 210K en Enero 2018"    
cb.set_label(Unit)


canal=('%02d' %icanal)
t_ini=minimo.GetMetadata()['date_created']    
date = str(t_ini[0:10])
time = str(imagenes_plots[0][0:73][34:36]) + ":" + str(imagenes_plots[0][0:73][36:38])    
Title = " GOES-16 ABI Canal "+ canal + " " + date + " " + time + " UTC"

plt.savefig(folder+'Frecuencia_'+mes+'.png', dpi=300,bbox_inches='tight', pad_inches=0)
    #plt.savefig(dire+'Channel_'+ canal+'_'+Region+'_'+date+'_'+time+'_WGS84.png', dpi=500,figsize=[20,16])

#############geotiff
# Export the result to GeoTIFF
driver = gdal.GetDriverByName('GTiff')
driver.CreateCopy(folder+'Frecuencia_'+mes+'.tif', grid_minimo, 0)



