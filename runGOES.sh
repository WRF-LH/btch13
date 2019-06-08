#!/bin/bash


echo "******************* DESCARGA ********************"

#/home/alighezzolo/BTCH13/DESCARGA/Amazon_down_scritp.sh $1 $2

echo "*******************LEVANTA SOURCE********************"

source activate GoesProcessAL

echo "*******************METADATOS GOES********************"

time python scr/GenMetadato_G16_CH13.py $1 $2

echo "*******************GRAFICA GOES********************"


time python scr/RUN_Graficardor_G16_CH13_VEC.py $1 $2


cd /home/sagus/Development/btch13/salidas/


ls | wc -l

echo "finnnnnnnnnn"
