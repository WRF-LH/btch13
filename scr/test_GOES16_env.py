# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""
mensaje = ""

try:
    from netCDF4 import Dataset
except ImportError:
    mensaje += "Falta o no funciona netCDF4\n"

try:
    import matplotlib.pyplot as plt # Import the Matplotlib package
except ImportError:
    mensaje += "Falta o no funciona matplotlib.pyplot\n"

try:
    from mpl_toolkits.basemap import Basemap # Import the Basemap toolkit
except ImportError:
    mensaje += "Falta o no funciona mpl_toolkits.basemap\n"

try:
    import numpy as np # Import the Numpy package
except ImportError:
    mensaje += "Falta o no funciona numpy\n"

try:
   from cpt_convert import loadCPT # Import the CPT convert function
except ImportError:
    mensaje += "Falta o no funciona cpt_convert\n"

try:
    from matplotlib.colors import LinearSegmentedColormap # Linear interpolation for color maps
except ImportError:
    mensaje += "Falta o no funciona matplotlib.colors\n"

try:
    from osgeo import osr,gdal
except ImportError:
    mensaje += "Falta o no funciona osgeo\n"

try:
    import time as t
except ImportError:
    mensaje += "Falta o no funciona time\n"

try:
    import calendar
except ImportError:
    mensaje += "Falta o no funciona calendar\n"

try:
    import sys
except ImportError:
    mensaje += "Falta o no funciona sys\n"

try:    
    from matplotlib.patches import Rectangle # Library to draw rectangles on the plot
except ImportError:
    mensaje += "Falta o no funciona matplotlib.patches\n"

try:
    import os 
except ImportError:
    mensaje += "Falta o no funciona os\n"

    
if (mensaje==''):
	print ('Esta todo listo para comenzar a trabajar!')
else:
	print(mensaje)
