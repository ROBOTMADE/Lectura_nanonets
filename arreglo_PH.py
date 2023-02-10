import pandas as pd
from config import *
from tqdm import tqdm
print("Leyendo archivo")
archivo = pd.read_excel("Salida/6/prueba_multilineaV2.xlsx", index_col= None)
descripciones_tr = []
codigos_barra_tr = []
promociones = []
descripcion_factura_esperada =[]
stop_words = ["(", ")", "[" , "]"]
replaces = {"PH":"PAPEL","COMPLET":"COMPLETO","COMPLETOO":"COMPLETO", "CUI": "CUIDADO", "COMPLE": "COMPLETO","COMPLEX": "COMPLETO",
            "DESINF":"DESINFECTANTE","ULT":"ULTRA","COLG":"COLGATE","EXT":"EXTRA","FABUL":"FABULOSO", "ALT":"ALTERNATIVA","HIG":"HIGIENICO",
            "CUID":"CUIDADO","DOB":"DOBLE","COMP":"COMPLETO","PEQ":"PEQUEÑO","PARRI":"PARRILLA","DESMANCH": "DESMANCHADOR"}
for index, row in tqdm(archivo.iterrows(), total= archivo.shape[0]):
    try:
        if index in([42,43,44]):
            print()
            print()
        descripcion_factura = str(row["descripcion"]).upper()
        for i in stop_words:
            descripcion_factura = descripcion_factura.replace(i, "")
        response_mailisearch = client.index('TR_ph_v2').search(descripcion_factura)
        producto_mailisearch = response_mailisearch['hits'][0]
        descripciones_tr.append(producto_mailisearch['Descripciones TR'])
        codigos_barra_tr.append(producto_mailisearch['Codigos de barras TR'])
        promociones.append(producto_mailisearch['Tipo promocion'])
        descripcion_factura_esperada.append(producto_mailisearch['Descripcion en factura'])
    except Exception as e:
        descripciones_tr.append('No Encontrado')
        codigos_barra_tr.append('No Encontrado')
        promociones.append('No Encontrado')
        descripcion_factura_esperada.append("No Encontrado")
archivo["Descricion_tr_nuevo_match_ph"] = descripciones_tr
archivo['Codigos_barra_tr_nuevo_match_ph'] = codigos_barra_tr
archivo['Promociones_tr_nuevo_match_ph'] = promociones
archivo["Descripcion en factura"] = descripcion_factura_esperada
#---------------------------------------------------------------------------------------------------------------------
analisis_rollos = pd.read_excel("Analisis de rollos.xlsx", index_col= None)
analisis_rollos = analisis_rollos[["Descripciones TR", "Codigos de barras TR", "Tipo promocion", "Rollo", "PROMOCION", "Detalle Promoción", "Descripcion en factura"]]

archivo_merge = archivo.merge(analisis_rollos, on ="Descripcion en factura" , how = "left")
#---------------------------------------------------------------------------------------------------------------------
archivo.to_excel(f"Salida/{version_lectura}/Match_Solr_New_Model_textos_procesados_match_Tiendas_TR_nuevo_ph_v5.xlsx", index=None)
archivo_merge.to_excel(f"Salida/{version_lectura}/Match_Solr_New_Model_textos_procesados_match_Tiendas_TR_nuevo_ph_v6.xlsx", index=None)

#---------------------------------------------------------------------------------------------------------------------