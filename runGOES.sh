#!/bin/bash

echo "*******************DESCARGA********************"

#/home/alighezzolo/BTCH13/DESCARGA/Amazon_down_scritp.sh $1 $2

echo "*******************LEVANTA SOURCE********************"

source activate GoesProcessAL

echo "*******************METADATOS GOES********************"

python GenMetadato_G16_CH13.py $1 $2

echo "*******************GRAFICA GOES********************"


python RUN_Graficardor_G16_CH13_VEC.py $1 $2

echo"*******************CALCULO DE LA MINIMA********************"

python Calculo_del_minimo_diario.py $1 $2

echo "*******************METADATO DE LA MINIMA********************"

python GenMetadato_Minimo_diario.py $1 $2

echo"*******************GRAFICO DE LA MINIMA********************"

python Calculo_minimo_diario_recorte_resultado.py $1 $2

echo "*******************BINARIZACION Y FRECUENCIA********************"

python Binarizar_por_umbral_frecuencia.py $1 $2

echo "*******************METADATO DE FRECUENCIA********************"

python GenMetadato_frecuencia_diario.py $1 $2

echo "*******************GRAFICO DE LA FRECUENCIA********************"

python Binarizar_por_umbral_frecuencia_recorte_resultado.py $1 $2


cd /home/alighezzolo/BTCH13/DATA/$1$2

echo "*******************NUMERO DE IMAGENES TRABAJADAS********************"


ls | wc -l

echo "finnnnnnnnnn"
