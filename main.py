import lectura_nanonets
import match_productos_general
import limpieza_general
import match_papel_higienico
from config import *
import pandas as pd
from tqdm import tqdm
###########################################################
#datos_nanonets = lectura_nanonets.procesar()
datos_nanonets =  pd.read_excel(f"Salida/6/Match_Solr_New_Model_textos_procesados_match_Tiendas_TR_nuevo_ph_v6.xlsx", index_col=None)

limpieza_general = limpieza_general.procesar(datos_nanonets)

datos_ph = match_papel_higienico.procesar(datos_nanonets)

datos_general = match_productos_general.procesar(datos_ph)

data_final = match_papel_higienico.limpieza_final(datos_general)
###############################################################
# ultima_factura = ""
#
# datos_nanonets =  pd.read_excel(f"Salida/{version_lectura}/lectura_nanonets.xlsx", index_col=None)
#


###############################################################
#numero de muestras = 727
#Facturas buenas de la muestra = 696
#Facturas malas de la muestra = 31
