import pandas as pd
from config import *

data_original = pd.read_excel(f"Salida/{version_lectura}/Entrega10FebreroV2.xlsx", index_col =None)
data_revisada = pd.read_excel("09-02-2023Match_Solr_New_Model_textos_procesados_match_Tiendas_TR_nuevo_ph_v2.xlsx", index_col= None)
data_unida = data_original.merge(data_revisada, on ="descripcion", how= "left")

data_unida.loc[data_unida["Tipo"] == 1, "Descricion_tr_nuevo_match_ph"] = "No Encontrado"
data_unida.loc[data_unida["Tipo"] == 1, "Codigos_barra_tr_nuevo_match_ph"] = "No Encontrado"
data_unida.loc[data_unida["Tipo"] == 1, "Promociones_tr_nuevo_match_ph"] = "No Encontrado"

data_eliminada = data_unida[data_unida["Tipo"] != 2]

data_eliminada.loc[data_unida["Tipo"] == 3, "Descricion_tr_nuevo_match_ph"] = "Es de PH pero no identifico cual"
data_eliminada.loc[data_unida["Tipo"] == 3, "Codigos_barra_tr_nuevo_match_ph"] = "Es de PH pero no identifico cual"
data_eliminada.loc[data_unida["Tipo"] == 3, "Promociones_tr_nuevo_match_ph"] = "Es de PH pero no identifico cual"

data_eliminada.to_excel("Data_reunion_10_febrero_revision_tipo.xlsx", index=None)