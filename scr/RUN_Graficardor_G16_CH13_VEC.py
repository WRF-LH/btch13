#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 1 11:59:10 2018

@author: Sergio

Basado en test5d.py

Lee los datos a partir de el archivo de metadatos generados previamente con
    GenMetadato_Goes16_v1.py

Calibra a Tb [Rad]->[C](lee los coeficiente de calibracion del
archivo auxiliar)

Reproyecta a WGS84, mediante Gdal dentro de Spyder

Grafica en los limites aproximados definidos por el SMN

Elije la paleta en funcion del canal

Genera un Geotiff

"""
# Required libraries

from mpl_toolkits.basemap import Basemap  # Import the Basemap toolkit
from cpt_convert import loadCPT  # Import the CPT convert function
from matplotlib.colors import LinearSegmentedColormap   # Linear interpolation
from osgeo import osr, gdal
from matplotlib.patches import Rectangle    # Library to draw rectangles
import numpy as np  # Import the Numpy package
import matplotlib.pyplot as plt  # Import the Matplotlib package
import time as t
import calendar
import sys
import os


def fecha(t0):
    """
    Dado un t0 en segundos, devuelve un par de strings de 
    fecha para las figuras (fechaT) y nombres de los archivos (fechaN)

    Parametro
    ----------
    t0 : timestamp
        tiempo en segundos
    """

    mes = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep',
           'Oct', 'Nov', 'Dic']   
    fechaT = ('%i-%s-%02d %02d:%02d:%02d UTC' % (t.gmtime(t0)[0],
                                                 mes[t.gmtime(t0)[1]],
                                                 t.gmtime(t0)[1],
                                                 t.gmtime(t0)[3],
                                                 t.gmtime(t0)[4],
                                                 t.gmtime(t0)[5]))            
    fechaN = ('%i%02d%02d_%02d%02d%02d' % (t.gmtime(t0)[0], t.gmtime(t0)[1],
                                           t.gmtime(t0)[1], t.gmtime(t0)[3],
                                           t.gmtime(t0)[4], t.gmtime(t0)[5]))
    return fechaT, fechaN


def exportImage(image, path):
    driver = gdal.GetDriverByName('netCDF')
    return driver.CreateCopy(path, image, 0)


def getGeoT(extent, nlines, ncols):
    # Compute resolution based on data dimension
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3], 0, -resy]


# Parametros
# Define KM_PER_DEGREE
KM_PER_DEGREE = 111.32
# GOES-16 Extent (satellite projection) [llx, lly, urx, ury]
GOES16_EXTENT = [-5434894.885056, -5434894.885056,
                 5434894.885056, 5434894.885056]

Region = 'ARG'  # ARG:Argentina / SuA:Sud America

if Region == 'ARG':
    extent = [-76, -60, -51, -20]  # LONLEFT,LATDOWN,LONRIGHT,LATUP
elif Region == 'SuA':
    extent = [-140, -60, -30, -5]
else:
    print("Error de definicion en la region, debe ser ARG o SuA")
    sys.exit(0)
    
resolution = 1.

# nombrevo a procesar
# dire='/mnt/E01498161497EE32/Users/Sergio/Conae/GRI/GOES_R/SMN/'
# dire='/mnt/E01498161497EE32/Users/Sergio/Conae/GRI/GOES_R/CUSS/'
# fechaDOY='2018002'#------------------------>>>> cambia dia a dia
fechaDOY = sys.argv[1] + sys.argv[2]

dire_out = '/home/alighezzolo/BTCH13/OUTPUTS/PNG/' + fechaDOY
+ '/' + os.makedirs(dire_out)

# dire='/media/andres/Elements/GOES16/BTCH13/IMAGENES/'+fechaDOY+'/'
dataPATH = '/home/alighezzolo/BTCH13/DATA/'+fechaDOY+'/'  # prueba andres

# dire='/media/andres/Elements/GOES16/descargas/20180630_granizo_goya_y_otros/CH13/'
dires = '/home/alighezzolo/BTCH13/SHAPES/'
direcpt = '/home/alighezzolo/BTCH13/CPT/'
# dire_out='/media/andres/Elements/GOES16/BTCH13/OUTPUTS/'+dia+'/nc/png/'

# nombre='OR_ABI-L1b-RadF-M3C01_G16_s20180961500406_e20180961511173_c20180961511217'
# nombre='OR_ABI-L1b-RadF-M3C02_G16_s20180961500406_e20180961511173_c20180961511211'
# nombre='OR_ABI-L1b-RadF-M3C03_G16_s20180961500406_e20180961511173_c20180961511220'
# nombre='OR_ABI-L1b-RadF-M3C04_G16_s20180961500406_e20180961511173_c20180961511197'
# nombre='OR_ABI-L1b-RadF-M3C05_G16_s20180961500406_e20180961511173_c20180961511218'
# nombre='OR_ABI-L1b-RadF-M3C06_G16_s20180961500406_e20180961511178_c20180961511215'
# nombre='OR_ABI-L1b-RadF-M3C07_G16_s20180961500406_e20180961511184_c20180961511220'
# nombre='OR_ABI-L1b-RadF-M3C08_G16_s20180961500406_e20180961511173_c20180961511220'
# nombre='OR_ABI-L1b-RadF-M3C09_G16_s20180961500406_e20180961511178_c20180961511238'
# nombre='OR_ABI-L1b-RadF-M3C10_G16_s20180961500406_e20180961511184_c20180961511233'
# nombre='OR_ABI-L1b-RadF-M3C11_G16_s20180961500406_e20180961511173_c20180961511232'
# nombre='OR_ABI-L1b-RadF-M3C12_G16_s20180961500406_e20180961511178_c20180961511229'
# nombre='OR_ABI-L1b-RadF-M3C13_G16_s20180961500406_e20180961511184_c20180961511236'
# nombre='OR_ABI-L1b-RadF-M3C14_G16_s20180951215403_e20180951226170_c20180951226236'
# nombre='OR_ABI-L1b-RadF-M3C14_G16_s20180961500406_e20180961511173_c20180961511238'
# nombre='OR_ABI-L1b-RadF-M3C15_G16_s20180961500406_e20180961511178_c20180961511237'
# nombre='OR_ABI-L1b-RadF-M3C16_G16_s20180961500406_e20180961511184_c20180961511235'
# nombre='OR_ABI-L2-CMIPF-M3C01_G16_s20181781415384_e20181781426151_c20181781426227'


def ploteador(nombre):  
    # archi=dire+nombre+'.nc'
    # archiM=dire+nombre+'.txt'
    archi = dataPATH + nombre  # archi=dire+nombre+'.nc'
    archiM = dataPATH + nombre[0:73] + '.txt'
    
    if (nombre[8] == '1'):
        VAR = nombre[11:14]
    elif(archi[8] == '2'):
        VAR = nombre[10:13]
    VAR = 'CMI'
    
    start = t.time()
        
    # %% Lectura de Metadatos
    
    arch = open(archiM, 'r')
    lines = arch.readlines()
    icanal = int(lines[3].split('#')[0])
    cols = int(lines[5].split('#')[0])
    rows = int(lines[6].split('#')[0])
    t_0 = float(lines[12].split('#')[0])
    t_start = lines[13][14:33]  # Fecha correspondiente a 0s
    
    # Parametross de calibracion
    offset = float(lines[25].split('#')[0])  # DN->L
    scale = float(lines[26].split('#')[0])
    
    esun = float(lines[28].split('#')[0])
    kapa0 = float(lines[30].split('#')[0])  # L->reflectancia
    ukapa0 = lines[31].split('#')[0]  # unidades
                
    fk1 = float(lines[34].split('#')[0])  # DN->K
    fk2 = float(lines[36].split('#')[0])
    bc1 = float(lines[38].split('#')[0])
    bc2 = float(lines[40].split('#')[0])            
    
    # Parametros de proyeccion
    proj = lines[14].split('#')[0]
    lat_0 = lines[19].split('#')[0]
    lon_0 = lines[20].split('#')[0]
    h = lines[21].split('#')[0]
    a = lines[22].split('#')[0]
    b = lines[23].split('#')[0]
    f = 1 / float(lines[24].split('#')[0])
    
    arch.close
              
    # %%Configuraciones espec'ificas para cada banda
    
    canal = ('%02d' % icanal)
    if icanal > 11:
        cptfile = 'IR4AVHRR6.cpt'
    elif icanal > 7:
        cptfile = 'SVGAWVX_TEMP.cpt'
    else:    
        cptfile = 'SVGAIR2_TEMP.cpt'
    
    print(cptfile)
    
    # %% lectura y extraccion de informacion de la pasada
    connectionInfo = 'HDF5:\"' + archi + '\"://'+VAR
        
    raw = gdal.Open(connectionInfo, gdal.GA_ReadOnly)
    
    driver = raw.GetDriver().LongName
    
    band = raw.GetRasterBand(1)
    bandtype = gdal.GetDataTypeName(band.DataType)
    print(bandtype)
    # data = band.ReadAsArray(0, 0, cols, rows)
    data = band.ReadAsArray()
    
    #  %% Proyecciones
    
    # GOES-16 Spatial Reference System
    sourcePrj = osr.SpatialReference()
    # sourcePrj.ImportFromProj4('+proj='+proj+' +h='+h+' +a='+a+' +b='+b+' +
    # f='+str(f)#no es valida proj+'geostationary'
    #             +'lat_0='+lat_0+' +lon_0='+lon_0+' +sweep=x +no_defs')  
    
    sourcePrj.ImportFromProj4('+proj=geos +h=' + h + ' +a=' + a + ' +b=' +
                              b + '  +f=' + str(f) + 'lat_0=' + lat_0 +
                              ' +lon_0=' + lon_0 + ' +sweep=x +no_defs')
    
    # Lat/lon WSG84 Spatial Reference System
    targetPrj = osr.SpatialReference()
    targetPrj.ImportFromProj4('+proj=longlat +ellps=WGS84 \
                               +datum=WGS84 + no_defs')
    
    # Setup projection and geo-transformation
    raw.SetProjection(sourcePrj.ExportToWkt())
    raw.SetGeoTransform(getGeoT(GOES16_EXTENT, raw.RasterYSize, 
                        raw.RasterXSize))
            
    # Compute grid dimension
    sizex = int(((extent[2] - extent[0]) * KM_PER_DEGREE) / resolution)
    sizey = int(((extent[3] - extent[1]) * KM_PER_DEGREE) / resolution)
        
    # Get memory driver
    memDriver = gdal.GetDriverByName('MEM')
       
    # Create grid
    grid = memDriver.Create('grid', sizex, sizey, 1, gdal.GDT_Float32)
        
    # Setup projection and geo-transformation
    grid.SetProjection(targetPrj.ExportToWkt())
    grid.SetGeoTransform(getGeoT(extent, grid.RasterYSize, grid.RasterXSize))
    
    # Perform the projection/resampling 
    gdal.ReprojectImage(raw, grid, sourcePrj.ExportToWkt(),
                        targetPrj.ExportToWkt(),
                        gdal.GRA_NearestNeighbour,
                        options=['NUM_THREADS=ALL_CPUS'])
              
    # Read grid data
    array1 = grid.ReadAsArray()
      
    # Mask fill values (i.e. invalid values)
    np.ma.masked_where(array1, array1 == -1, False)
        
    # %% Calibracion
    array = array1 * scale + offset  # DN ->mW m-2 sr-1 mum-1
    # if icanal>=7:#DN ->C
    #    Temp=(fk2 / (np.log((fk1 / array) + 1)) - bc1 ) / 
    #    bc2-273.15#mW m-2 sr-1 mum-1 ->C
    # else:
    #    Temp=kapa0*array#REVISAR!!!
    Temp = array - 273.15
    # Temp=array
        
    grid.GetRasterBand(1).SetNoDataValue(-1)
    grid.GetRasterBand(1).WriteArray(array)
    
    # %% Plot the Data ========================================================
    # Create the basemap reference for the Rectangular Projection
    
    t_ini = t_0 + float(calendar.timegm(t.strptime(t_start, 
                        '%Y-%m-%d %H:%M:%S')))
    fechaT, fechaN = fecha(t_ini)  # Fechas para titulos y nombre de archivo
    
    fig = plt.figure(num=1, clear='True')
    # frameon es para NO desplegar la figura
    fig = plt.figure(num=1, figsize=[20, 16], dpi=300, frameon='False')
    # 4326 es WGS84 (LatLOn)
    bmap = Basemap(resolution='h', llcrnrlon=extent[0], llcrnrlat=extent[1],
                   urcrnrlon=extent[2], urcrnrlat=extent[3], epsg=4326)
     
    # Draw the shapefiles
    bmap.readshapefile(dires+'008_limites_provinciales_LL', 
                       '008_limites_provinciales_LL', linewidth=0.3, color='w')
    bmap.readshapefile(dires+'DEPARTAMENTOS_linea', 'DEPARTAMENTOS_linea',
                       linewidth=0.1, color='gray')
    # bmap.readshapefile(dires3+'Límites_internacionales','Límites_internacionales',linewidth=0.3,color='w')
    # bmap.readshapefile(dires+'Ejidos_urbanos_linea','Ejidos_urbanos_linea',linewidth=0.1,color='yellow')#bmap.readshapefile(dires3+'Límites_internacionales','Límites_internacionales',linewidth=0.3,color='w')
    # bmap.readshapefile(dires+'Lago_San_Roque','Lago_San_Roque',linewidth=0.5,color='blue')#bmap.readshapefile(dires3+'Límites_internacionales','Límites_internacionales',linewidth=0.3,color='w')
    # bmap.readshapefile(dires+'Ejidos_afectados_linea','Ejidos_afectados_linea',linewidth=0.7,color='w')#bmap.readshapefile(dires3+'Límites_internacionales','Límites_internacionales',linewidth=0.3,color='w')       
    # bmap.readshapefile(dires+'Zona_Afectada_EPSG4326_linea','Zona_Afectada_EPSG4326_linea',linewidth=0.7,color='w')#bmap.readshapefile(dires3+'Límites_internacionales','Límites_internacionales',linewidth=0.3,color='w')       
    # bmap.readshapefile(dires+'ne_10m_admin_0_map_units/ne_10m_admin_0_map_units','ne_10m_admin_0_map_units',linewidth=0.3,color='w')
    # bmap.readshapefile(dires+'limite_interprovincial/Límites_interprovinciales','Límites_interprovinciales',linewidth=0.3,color='w')
    # bmap.readshapefile(dires3+'Límites_internacionales','Límites_internacionales',linewidth=0.3,color='w')
     
    # Draw parallels and meridians
    bmap.drawparallels(np.arange(-90.0, 90.0, 3.), linewidth=0.3, 
                       dashes=[4, 4], color='white', labels=[True, 
                       True, False, False], fmt='%g', labelstyle="+/-", 
                       xoffset=0.10, yoffset=-1.00, size=5)
    bmap.drawmeridians(np.arange(0.0, 360.0, 3.), linewidth=0.3, 
                       dashes=[4, 4], color='white', labels=[False,
                       False, True, False], fmt='%g', labelstyle="+/-", 
                       xoffset=-0.80, yoffset=0.20, size=5)
     
    # Converts a CPT file to be used in Python
    # cptfile = "crisp_ice.cpt"
    cpt = loadCPT(direcpt+cptfile)
    
    # Makes a linear interpolation
    cpt_convert = LinearSegmentedColormap('cpt', cpt)
     
    # Plot the GOES-16 channel with the converted CPT colors (you may alter 
    # the min and max to match your preference)
    if icanal >= 7:
        img_plot = bmap.imshow(Temp, origin='upper', cmap=cpt_convert, 
                               vmin=-90, vmax=50)
    else:
        img_plot = bmap.imshow(Temp, origin='upper', cmap='Greys', 
                               vmin=0.001, vmax=0.1)  # 'Greys'
    
    # Add a black rectangle in the bottom to insert the image description
    lon_difference = (extent[2] - extent[0])  # Max Lon - Min Lon
    currentAxis = plt.gca()
    currentAxis.add_patch(Rectangle((extent[0], extent[1]), lon_difference, 
                          (lon_difference) * 0.040, alpha=1, zorder=3, 
                          facecolor='black'))
    
    if icanal >= 7:
        Unit = "Temperatura de Brillo [°C]"
    else:
        Unit = "Reflectancia"
    
    t_ini = raw.GetMetadata()['date_created']    
    date = str(t_ini[0:10])
    time = str(nombre[34:36]) + ":" + str(nombre[36:38])
    Title = " GOES-16 ABI Canal " + canal + " " + date + " " + time + " UTC"
    
    # Title = " GOES-16 ABI Canal "+ canal +" "+ fechaT
    Institution = "CONAE-Argentina"
    
    # Add the image description inside the black rectangle
    lat_difference = (extent[3] - extent[1])  # Max lat - Min lat
    plt.text(extent[0], extent[1] + lat_difference * 0.005, Title, 
             horizontalalignment='left', color='white', size=5)
    plt.text(extent[2], extent[1] + lat_difference * 0.005, Institution, 
             horizontalalignment='right', color='white', size=5)
    
    # Insert the colorbar at the right
    cb = bmap.colorbar(location='bottom', size='2%', pad='1%')
    cb.outline.set_visible(True)  # Remove the colorbar outline
    cb.ax.tick_params(width=0)  # Remove the colorbar ticks
    cb.ax.xaxis.set_tick_params(pad=-2)  # Put the colobar labels inside
    # the colorbar
    cb.ax.tick_params(axis='x', colors='black', labelsize=6)  # Change the
    # color and size of the colorbar labels
    
    cb.set_label(Unit)
     
    # Export the result to GeoTIFF
    # driver = gdal.GetDriverByName('GTiff')
    # driver.CreateCopy(dire+'Channel_'+ canal+'_'+
    # Region+fechaN+'_WGS84.tif', grid, 0)
    
    # grabar a png

    # Volver este
    # plt.savefig(dire_out+'Channel_'+ canal+'_'+Region+'_'+
    # date+'_'+time+'_WGS84.png', 
    # dpi=300,bbox_inches='tight', pad_inches=0)
    # dire_out2='/media/andres/Elements/GOES16/BTCH13/ANTARTIDA/'
    plt.savefig(dire_out+'Channel_' + canal+'_' + Region + '_' + date +
                '_' + time + '_WGS84.png', dpi=300, bbox_inches='tight',
                pad_inches=0)
    
    # plt.savefig(dire+'Channel_'+ canal+'_'+Region+'_'+date+'_'+time+
    # '_WGS84.png', dpi=500,figsize=[20,16])
    
    # Close file
    raw = None
    print('- finished! Time:', t.time() - start, 'seconds')
    # ##############################################################GEOTIFF
    # grid.GetRasterBand(1).WriteArray(array)
    # driver = gdal.GetDriverByName('GTiff')
    # driver.CreateCopy(dire_out+'Channel_'+ canal+'_'+Region+'_'+date+'_'+
    # time+'_WGS84.tif', grid, 0)


# ####carga de imagenes
files = os.listdir(dataPATH)
for file in files:
    if not file.endswith(".nc"):
        continue
    print('*'*200 + file)
    ploteador(file)
    