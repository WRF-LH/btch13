#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import geopandas as gpd
import pandas as pd
import rasterio
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from rasterstats import zonal_stats

fechaDOY = sys.argv[1]+sys.argv[2]

gdf = gpd.read_file('/home/andres/GOES16/SHAPES/departamentos.shp',
                    encoding='utf-8')

dire = '/home/andres/GOES16/DATATMP/'


def proccess(raster_name):
    # raster_name='Channel_13_ARG_2019-04-05_00:00_WGS84.tif'
    # raster =rasterio.open('/home/andres/GOES16/OUTPUTS/'+fechaDOY+
    # '/'+raster_name)
    raster_path = dire+raster_name
    raster = rasterio.open(raster_path)
    affine = raster.transform
    array = raster.read(1)

    df_zonal_stats = pd.DataFrame(zonal_stats(gdf, array, affine=affine,
                                              all_touched=True))

    # adding statistics back to original GeoDataFrame
    gdf2 = pd.concat([gdf, df_zonal_stats], axis=1)
    gdf2 = gdf2[gdf2['DEPARTAMTO'] != 'ANTARTIDA ARGENTINA'][gdf2['DEPARTAMTO']
                                   != 'ISLAS SANDWICH DEL'][gdf2['DEPARTAMTO']
                                   != 'ISLAS GEORGIAS DEL SUR']

    f, ax = plt.subplots(1, figsize=(20, 16))
    ax.axis('off')

    cm = LinearSegmentedColormap.from_list('cm', [(1, 0, 0),
                                                  (1, 50/256, 50/256),
                                                  (1, 100/256, 100/256),
                                                  (1, 150/256, 150/256),
                                                  (1, 200/256, 200/256),
                                                  (1, 250/256, 250/256),
                                                  (1, 1, 1)],
                                           N=6)

    gdf2.plot(column='min', cmap=cm, vmin=190, vmax=220, ax=ax,
              edgecolor='#000000', linewidth=0.05, legend=True)

    plt.title('Departamentos bajo el umbral de 215 K', fontsize='30')
    f.text(0.77, 0.5, 'Temperatura de Brillo (ºK)', size=24, ha='center',
           va='center', rotation=90)
    fecha = raster_name[15:25]
    hora = raster_name[26:31]
    titulo = 'Producto experimental - CH13 - '+fecha+' '+hora+'UTC'
    f.text(0.55, 0.12, str(titulo), size=15, ha='center', va='center',
           rotation=0)

    provincias = gpd.read_file('/home/andres/GOES16/SHAPES/\
                                008_limites_provinciales.shp')

    provincias.plot(ax=ax, edgecolor='#000000', linewidth=0.2, color='None')

    canal = '13'
    Region = 'ARG'
    date = raster_name[15:31]

    plt.savefig('/home/andres/GOES16/OUTPUTS/'+fechaDOY+'/Channel_'
                + canal + '_' + Region+'_'+date+'_WGS84_DEPTO.png',
                dpi=150, bbox_inches='tight')


files = os.listdir(dire)
for file in files:
    if not file.endswith(".tif"):
        continue
    print('*'*200 + file)
    proccess(file)
