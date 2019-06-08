#!/bin/bash


# DIRECTORIOS
export GOES_OP=$HOME/goes-operativo
export GOES_DATA=/home/datos/goes_16
export EJECUTABLES=$GOES_OP/ejecutables
export DATOS=$GOES_OP/datos
export SALIDAS=/home/datos/goes_16/salidas
export LOGS=$GOES_OP/salidas/logs


# DATOS DE DESCARGA
export CHANNELS='C01 C02 C03 C08 C09 C10 C13' # Ejemplo: CHANNELS='C01 C02 C03 C04 C05 C06 C07 C08 C09 C10 C11 C12 C13 C14 C15 C16'
export PRODUCTS='L2-CMIPF' # Ejemplo: PRODUCTS='L1b-RadC L1b-RadF L1b-RadM L2-CMIPC L2-CMIPF L2-CMIPM L2-MCMIPC L2-MCMIPF L2-MCMIPM'

# DATOS DE GRAFICO
export LON_MIN=-75
export LON_MAX=-58 #-50 #58
export LAT_MIN=-40 #40
export LAT_MAX=-25

export LON_MIN_WEBMET=-77
export LON_MAX_WEBMET=-51
export LAT_MIN_WEBMET=-56
export LAT_MAX_WEBMET=-20

#export PATH="/home/goes/anaconda3/bin:$PATH"
source ~/anaconda3/etc/profile.d/conda.sh
conda activate goes-operativo
