#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Levanta todos los parametros con NETCDF y escribe algunos en un archivo
de metadato
Se reagrupan segun de que se tratan
Se presentan primero los valores numericos (o string), luego con # el nombre de
 la variable original y eventualmente una explicacion

http://geoinformaticstutorial.blogspot.com.ar/2012/09/reading-raster-data-with-python-and-gdal.html

Groseramente modificado por AL para procesar estadisticas de GOES-16
"""
# Required libraries
from netCDF4 import Dataset
import os
import sys


#dia = sys.argv[1]+sys.argv[2]


SHAPEFILES = os.environ['GOES_DATA'] + '/shapefiles'
logo = os.environ['GOES_DATA'] + '/img/wug_txt2.png'
#DATA = os.environ[]
dire = '/mnt/datos/goes_16/datos/casos/2019-03-30-31_RRQPOE/'  # prueba andres


def ploteador(archi):
    path = dire+archi

    # %% Lee NETCDF
    #g16nc = Dataset(path, 'r')

    # Explora las variables
    dataset = Dataset(dire+archi)
    print(dataset.file_format)
    variables = dataset.variables.keys()  # lista las variables

    for v in variables:
        print("%s %s" % (v, dataset.variables[v]))

    # band_id = dataset.variables['band_id'][:]
    # band_wavelength = dataset.variables['band_wavelength'][:]

    # %% Escribe en un archivo todos los datos
    archi2 = archi[:-2]+'txt'

   # Informacion general
    f = open(dire+archi2, 'w')
    f.write("%s #%s\n" % (dataset.file_format, 'Formato del archivo original'))
    f.write("%s #%s\n" % (dataset.variables['CMI'].long_name,
                          "Nombre del producto"))
    f.write("%s #%s\n" % (dataset.variables['CMI'].standard_name,
                          "Nombre del producto"))
    f.write("%d #%s\n" % (dataset.variables['band_id'][:][0],
                          dataset.variables['band_id'].long_name))
    f.write("%f #%s\n" % (dataset.variables['band_wavelength'][:][0],
                          dataset.variables['band_wavelength'].long_name))
    f.write("%s #%s\n" % (dataset.variables['x'].shape[0],
                          "Numero de columnas"))
    f.write("%s #%s\n" % (dataset.variables['y'].shape[0],
                          "Numero de filas"))
    f.write("%s #%s\n" % (dataset.variables['CMI'].sensor_band_bit_depth,
                          "Numero de bits"))
    f.write("%f #%s\n" % (dataset.variables['x'].scale_factor,
                          "Resolucion en x"))
    f.write("%s #%s\n" % (dataset.variables['x'].units,
                          "Unidades en x"))
    f.write("%f #%s\n" % (dataset.variables['y'].scale_factor,
                          "Resolucion en y"))
    f.write("%s #%s\n" % (dataset.variables['y'].units,
                          "Unidades en y"))

    f.write("%f #%s\n" % (dataset.variables['t'][0], "Tiempo"))
    f.write("%s #%s\n" % (dataset.variables['t'].units, "Unidades de tiempo"))

    # Parametros geometricos  y de proyeccion
    f.write("%s #%s\n" % (dataset.variables['goes_imager_projection'].
                          grid_mapping_name, " Tipo de proyeccion "))

    f.write("%s #%s\n" % (dataset.variables['geospatial_lat_lon_extent'].
                          getncattr('geospatial_westbound_longitude'),
                          "Limite Oeste"))
    f.write("%s #%s\n" % (dataset.variables['geospatial_lat_lon_extent'].
                          getncattr('geospatial_eastbound_longitude'),
                          "Limite Este"))
    f.write("%s #%s\n" % (dataset.variables['geospatial_lat_lon_extent'].
                          getncattr('geospatial_northbound_latitude'),
                          "Limite Norte"))
    f.write("%s #%s\n" % (dataset.variables['geospatial_lat_lon_extent'].
                          getncattr('geospatial_southbound_latitude'),
                          "Limite Sur"))
    f.write("%s #%s\n" % (dataset.variables['geospatial_lat_lon_extent'].
                          getncattr('geospatial_lat_center'),
                          "Latitud central"))
    f.write("%s #%s\n" % (dataset.variables['geospatial_lat_lon_extent'].
                          getncattr('geospatial_lon_center'),
                          "Longitud central"))

    f.write("%f #%s\n" % (dataset.variables['goes_imager_projection'].
                          getncattr('perspective_point_height'), "Altura"))
    f.write("%s #%s\n" % (dataset.variables['goes_imager_projection'].
                          getncattr('semi_major_axis'), "Semi eje mayor"))
    f.write("%s #%s\n" % (dataset.variables['goes_imager_projection'].
                          getncattr('semi_minor_axis'), "Semi eje menor"))
    f.write("%s #%s\n" % (dataset.variables['goes_imager_projection'].
                          getncattr('inverse_flattening'),
                          "Achatamiento inverso"))

    # Parametros de calibracion
    f.write("%f #%s\n" % (dataset.variables['CMI'].
                          add_offset, "Offset"))
    f.write("%f #%s\n" % (dataset.variables['CMI'].
                          scale_factor, "Factor de escala"))
    f.write("%s #%s\n" % (dataset.variables['CMI'].
                          units, "Unidades"))
    f.write("%f #%s\n" % (dataset.variables['esun'][0], dataset.variables
            ['esun'].long_name))
    f.write("%s #%s\n" % (dataset.variables['esun'].units, "Unidades"))
    f.write("%f #%s\n" % (dataset.variables['kappa0'][0], dataset.variables
            ['kappa0'].long_name))
    f.write("%s #%s\n" % (dataset.variables['kappa0'].units, "Unidades"))
    f.write("%f #%s\n" % (dataset.
                          variables['earth_sun_distance_anomaly_in_AU'][0],
                          dataset.
                          variables['earth_sun_distance_anomaly_in_AU'].
                          long_name))
    f.write("%s ##%s\n" % (dataset.
                           variables['earth_sun_distance_anomaly_in_AU'].
                           units, "Unidades"))
    f.write("%f #%s\n" % (dataset.variables['planck_fk1'][0], dataset.variables
            ['planck_fk1'].long_name))
    f.write("%s #%s\n" % (dataset.variables['planck_fk1'].units, "Unidades"))
    f.write("%f #%s\n" % (dataset.variables['planck_fk2'][0], dataset.variables
            ['planck_fk1'].long_name))
    f.write("%s #%s\n" % (dataset.variables['planck_fk2'].units, "Unidades"))
    f.write("%f #%s\n" % (dataset.variables['planck_bc1'][0], dataset.variables
            ['planck_bc1'].long_name))
    f.write("%s #%s\n" % (dataset.variables['planck_bc1'].units, "Unidades"))
    f.write("%f #%s\n" % (dataset.variables['planck_bc2'][0], dataset.variables
            ['planck_bc2'].long_name))
    f.write("%s #%s\n" % (dataset.variables['planck_bc2'].units, "Unidades"))


files = os.listdir(dire)
for file in files:
    if not file.endswith(".nc"):
        continue
    print('*'*200 + file)
    ploteador(file)
