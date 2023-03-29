import match_productos_general
import limpieza_general
from Lectura_facturas.git.Lectura_nanonets import match_papel_higienico
import arreglo_PH
import dinamicas_promocionales
import normalizacion_numericos
import lectura_nanonets
from config import *
import pandas as pd
###########################################################
datos_nanonets = lectura_nanonets.procesar()
#datos_nanonets =  pd.read_excel(f"Salida/{version_lectura}/lectura_nanonets.xlsx", index_col=None)
limpieza_general = limpieza_general.procesar(datos_nanonets)
normalizacion = normalizacion_numericos.procesar(limpieza_general)
datos_ph = arreglo_PH.procesar(limpieza_general)
#datos_ph = match_papel_higienico.procesar(datos_nanonets)
datos_general = match_productos_general.procesar(datos_ph)
data_con_dinamicas = dinamicas_promocionales.procesar(datos_general)
data_final = match_papel_higienico.limpieza_final(datos_general)
###############################################################
# ultima_factura = ""
#
# datos_nanonets = pd.read_excel(f"Salida/{version_lectura}/lectura_nanonets.xlsx", index_col=None)
#
###############################################################
#numero de muestras = 727
#Facturas buenas de la muestra = 696
#Facturas malas de la muestra = 31