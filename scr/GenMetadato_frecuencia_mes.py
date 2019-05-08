#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:59:10 2018

@author: Sergio

Basado en test6a 
Levanta todos los parametros con NETCDF y escribe algunos en un archivo de metadato
Se reagrupan segun de que se tratan
Se presentan primero los valores numericos (o string), luego con # el nombre de
 la variable original y eventualmente una explicacion  


http://geoinformaticstutorial.blogspot.com.ar/2012/09/reading-raster-data-with-python-and-gdal.html


"""
 
# Required libraries
from netCDF4 import Dataset
import os

#Parametros basicos
#dire='/mnt/E01498161497EE32/Users/Sergio/Conae/GRI/GOES_R/CUSS/'

mes='201801'#---------------------------------------------------->>>> cambia dia a dia

dire='/home/alighezzolo/BTCH13/OUTPUTS/NC/'+mes+'/'


#archi='OR_ABI-L1b-RadF-M3C01_G16_s20180961500406_e20180961511173_c20180961511217.nc'
#archi='OR_ABI-L1b-RadF-M3C02_G16_s20180961500406_e20180961511173_c20180961511211.nc'
#archi='OR_ABI-L1b-RadF-M3C03_G16_s20180961500406_e20180961511173_c20180961511220.nc'
#archi='OR_ABI-L1b-RadF-M3C04_G16_s20180961500406_e20180961511173_c20180961511197.nc'
#archi='OR_ABI-L1b-RadF-M3C05_G16_s20180961500406_e20180961511173_c20180961511218.nc'
#archi='OR_ABI-L1b-RadF-M3C06_G16_s20180961500406_e20180961511178_c20180961511215.nc'
#archi='OR_ABI-L1b-RadF-M3C07_G16_s20180961500406_e20180961511184_c20180961511220.nc'
#archi='OR_ABI-L1b-RadF-M3C08_G16_s20180961500406_e20180961511173_c20180961511220.nc'
#archi='OR_ABI-L1b-RadF-M3C09_G16_s20180961500406_e20180961511178_c20180961511238.nc'
#archi='OR_ABI-L1b-RadF-M3C10_G16_s20180961500406_e20180961511184_c20180961511233.nc'
#archi='OR_ABI-L1b-RadF-M3C11_G16_s20180961500406_e20180961511173_c20180961511232.nc'
#archi='OR_ABI-L1b-RadF-M3C12_G16_s20180961500406_e20180961511178_c20180961511229.nc'
#archi='OR_ABI-L1b-RadF-M3C13_G16_s20180961500406_e20180961511184_c20180961511236.nc'
#archi='OR_ABI-L1b-RadF-M3C14_G16_s20180951215403_e20180951226170_c20180951226236.nc'
#archi='OR_ABI-L1b-RadF-M3C14_G16_s20180961500406_e20180961511173_c20180961511238.nc'
#archi='OR_ABI-L1b-RadF-M3C15_G16_s20180961500406_e20180961511178_c20180961511237.nc'
#archi='OR_ABI-L1b-RadF-M3C16_G16_s20180961500406_e20180961511184_c20180961511235.nc'

#archi='OR_ABI-L1b-RadF-M3C13_G16_s20181661315417_e20181661326195_c20181661326252.nc'#prueba andres
#archi='OR_ABI-L2-CMIPF-M3C01_G16_s20181781415384_e20181781426151_c20181781426227.nc'

def ploteador(archi):    
    path=dire+archi
    
    
    
    
    #%% Lee NETCDF
    g16nc = Dataset(path, 'r')
    
    
    # Explora las variables
    
    dataset= Dataset(dire+archi)
    
    print(dataset.file_format)
    
    variables=dataset.variables.keys() #lista las variables
    
    for v in variables:
        print("%s %s" %(v,dataset.variables[v]) )
    
    band_id=dataset.variables['band_id'][:]
    
    band_wavelength=dataset.variables['band_wavelength'][:]
    
    
    #%% Escribe en un archivo todos los datos
    
    archi2=archi[:-2]+'txt'
    
    # Informacion general
    f = open (dire+archi2,'w')
    f.write("%s #%s\n" %(dataset.file_format,'Formato del archivo original'))
    f.write("%s #%s\n" %(dataset.variables['CMI'].long_name,"Nombre del producto"))
    f.write("%s #%s\n" %(dataset.variables['CMI'].standard_name,"Nombre del producto"))
    f.write("%d #%s\n" %(dataset.variables['band_id'][:][0],dataset.variables['band_id'].long_name))        
    f.write("%f #%s\n" %(dataset.variables['band_wavelength'][:][0],dataset.variables['band_wavelength'].long_name))
    f.write("%s #%s\n" %(dataset.variables['x'].shape[0],"Numero de columnas"))
    f.write("%s #%s\n" %(dataset.variables['y'].shape[0],"Numero de filas"))
    f.write("%s #%s\n" %(dataset.variables['CMI'].sensor_band_bit_depth,"Numero de bits"))
    f.write("%f #%s\n" %(dataset.variables['x'].scale_factor,"Resolucion en x"))
    f.write("%s #%s\n" %(dataset.variables['x'].units,"Unidades en x"))
    f.write("%f #%s\n" %(dataset.variables['y'].scale_factor,"Resolucion en y"))
    f.write("%s #%s\n" %(dataset.variables['y'].units,"Unidades en y"))
    
    f.write("%f #%s\n" %(dataset.variables['t'][0],"Tiempo"))
    f.write("%s #%s\n" %(dataset.variables['t'].units,"Unidades de tiempo"))
    
    # Parametros geometricos  y de proyeccion        
    f.write("%s #%s\n" %(dataset.variables['goes_imager_projection'].grid_mapping_name,
            " Tipo de proyeccion "))
    
    f.write("%s #%s\n" %(dataset.variables['geospatial_lat_lon_extent'].getncattr('geospatial_westbound_longitude')
            ,"Limite Oeste"))
    f.write("%s #%s\n" %(dataset.variables['geospatial_lat_lon_extent'].getncattr('geospatial_eastbound_longitude')
            ,"Limite Este"))
    f.write("%s #%s\n" %(dataset.variables['geospatial_lat_lon_extent'].getncattr('geospatial_northbound_latitude')
            ,"Limite Norte"))
    f.write("%s #%s\n" %(dataset.variables['geospatial_lat_lon_extent'].getncattr('geospatial_southbound_latitude')
            ,"Limite Sur"))
    f.write("%s #%s\n" %(dataset.variables['geospatial_lat_lon_extent'].getncattr('geospatial_lat_center')
            ,"Latitud central"))
    f.write("%s #%s\n" %(dataset.variables['geospatial_lat_lon_extent'].getncattr('geospatial_lon_center')
            ,"Longitud central"))
          
    f.write("%f #%s\n" %(dataset.variables['goes_imager_projection'].getncattr('perspective_point_height'),
            "Altura"))
    f.write("%s #%s\n" %(dataset.variables['goes_imager_projection'].getncattr('semi_major_axis'),
            "Semi eje mayor"))       
    f.write("%s #%s\n" %(dataset.variables['goes_imager_projection'].getncattr('semi_minor_axis'),
            "Semi eje menor"))    
    f.write("%s #%s\n" %(dataset.variables['goes_imager_projection'].getncattr('inverse_flattening'),
            "Achatamiento inverso"))  
    
    
    
    # Parametros de calibracion
    f.write("%f #%s\n" %(dataset.variables['CMI'].add_offset,"Offset"))
    f.write("%f #%s\n" %(dataset.variables['CMI'].scale_factor,"Factor de escala"))
    f.write("%s #%s\n" %(dataset.variables['CMI'].units,"Unidades"))        
    
    f.write("%f #%s\n" %(dataset.variables['esun'][0], dataset.variables
            ['esun'].long_name))
    f.write("%s #%s\n" %(dataset.variables['esun'].units,"Unidades"))        
    
    f.write("%f #%s\n" %(dataset.variables['kappa0'][0], dataset.variables
            ['kappa0'].long_name))
    f.write("%s #%s\n" %(dataset.variables['kappa0'].units,"Unidades"))     
    
    f.write("%f #%s\n" %(dataset.variables['earth_sun_distance_anomaly_in_AU'][0], dataset.variables
            ['earth_sun_distance_anomaly_in_AU'].long_name))
    f.write("%s ##%s\n" %(dataset.variables['earth_sun_distance_anomaly_in_AU'].units,"Unidades"))  
    
            
    f.write("%f #%s\n" %(dataset.variables['planck_fk1'][0], dataset.variables
            ['planck_fk1'].long_name))
    f.write("%s #%s\n" %(dataset.variables['planck_fk1'].units,"Unidades"))
    
    f.write("%f #%s\n" %(dataset.variables['planck_fk2'][0], dataset.variables
            ['planck_fk1'].long_name))
    f.write("%s #%s\n" %(dataset.variables['planck_fk2'].units,"Unidades"))
            
    f.write("%f #%s\n" %(dataset.variables['planck_bc1'][0], dataset.variables
            ['planck_bc1'].long_name))
    f.write("%s #%s\n" %(dataset.variables['planck_bc1'].units,"Unidades"))
    
    f.write("%f #%s\n" %(dataset.variables['planck_bc2'][0], dataset.variables
            ['planck_bc2'].long_name))
    f.write("%s #%s\n" %(dataset.variables['planck_bc2'].units,"Unidades"))
            
files=os.listdir(dire)
for file in files: 
    if not file.endswith(".nc"):
        continue
    print ('*'*200 + file)
    ploteador(file)
            
    
g16nc.close()        
f.close()
