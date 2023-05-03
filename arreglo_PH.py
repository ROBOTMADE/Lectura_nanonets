import re

import pandas as pd
from config import *
from tqdm import tqdm
import difflib
print("Leyendo archivo")

def procesar (df):
    archivo = df
    descripciones_tr = []
    codigos_barra_tr = []
    promociones = []
    descripcion_factura_esperada =[]
    stop_words = ["(", ")", "[" , "]","PPK"]
    bonificacion =[]
    palabras_inicio = ["BONI 1", "", "DESCRIPCIÓN ", "BONIF ", "* BONIF ", " BONIF ", "WW ", ". BONIF ", "ww" ,". * BONIF ", '" BONIF ', "BONI ", "PAC ", "BONI 1 " ". " ]
    regex_inicio = ["^([0-9]+.[0-9]+ )|^([0-9]+ )", "^\(.+\) ", "^\( [0-9]+ "]
    replaces = {"PH":"PAPEL","COMPLET":"COMPLETO","COMPLETOO":"COMPLETO", "CUI": "CUIDADO", "COMPLE": "COMPLETO","COMPLEX": "COMPLETO",
                "DESINF":"DESINFECTANTE","ULT":"ULTRA","COLG":"COLGATE","EXT":"EXTRA","FABUL":"FABULOSO", "ALT":"ALTERNATIVA","HIG":"HIGIENICO",
                "CUID":"CUIDADO","DOB":"DOBLE","COMP":"COMPLETO","PEQ":"PEQUEÑO","PARRI":"PARRILLA","DESMANCH": "DESMANCHADOR"}
    for index, row in tqdm(archivo.iterrows(), total= archivo.shape[0]):
        try:
            descripcion_factura = str(row["descripcion"]).upper()
            descripcion_factura = descripcion_factura.replace("+"," + ")
            for inicio in palabras_inicio:
                if descripcion_factura.startswith(inicio):
                    descripcion_factura = descripcion_factura.replace(inicio, "")

            for regex_inicial in regex_inicio:
                descripcion_factura = re.sub(regex_inicial, "", descripcion_factura)
            for i in stop_words:
                descripcion_factura = descripcion_factura.replace(i, "")

            response_mailisearch = client.index('TR_ph_v2').search(descripcion_factura)
            producto_mailisearch = response_mailisearch['hits'][0]
            descripcion_factura_comprobar  = producto_mailisearch["Descripcion en factura"]
            descripcion_factura_comprobar = descripcion_factura_comprobar.replace("+", " + ")
            for i in stop_words:
                descripcion_factura_comprobar = descripcion_factura_comprobar.replace(i, "")
            ratio_primera_letra = difflib.SequenceMatcher(None, f"{descripcion_factura_comprobar.split()[0]} {descripcion_factura_comprobar.split()[1]}", f"{descripcion_factura.split()[0]} {descripcion_factura.split()[1]}").ratio()
            if ratio_primera_letra > 0.35:
                descripciones_tr.append(producto_mailisearch['Descripciones TR'])
                codigos_barra_tr.append(producto_mailisearch['Codigos de barras TR'])
                promociones.append(producto_mailisearch['Tipo promocion'])
                descripcion_factura_esperada.append(producto_mailisearch['Descripcion en factura'])
            else:
                descripciones_tr.append('No Encontrado')
                codigos_barra_tr.append('No Encontrado')
                promociones.append('No Encontrado')
                descripcion_factura_esperada.append("No Encontrado")
        except Exception as e:
            descripciones_tr.append('No Encontrado')
            codigos_barra_tr.append('No Encontrado')
            promociones.append('No Encontrado')
            descripcion_factura_esperada.append("No Encontrado")
        inserte_bonificacion = False
        for word in palabras_bonificacion:
            if word in str(row["descripcion"]).upper():
                bonificacion.append("Posible Bonificacion")
                inserte_bonificacion = True
                break
        if not inserte_bonificacion:
            bonificacion.append("No posee bonificacion")

    archivo ["Bonificacion"] = bonificacion
    archivo["Descricion_tr_nuevo_match_ph"] = descripciones_tr
    archivo['Codigos_barra_tr_nuevo_match_ph'] = codigos_barra_tr
    archivo['Promociones_tr_nuevo_match_ph'] = promociones
    archivo["Descripcion en factura"] = descripcion_factura_esperada

    #---------------------------------------------------------------------------------------------------------------------
    analisis_rollos = pd.read_excel("Analisis de rollos.xlsx", index_col= None)
    analisis_rollos = analisis_rollos[["Descripciones TR", "Codigos de barras TR", "Tipo promocion", "Rollo", "PROMOCION", "Detalle Promoción", "Descripcion en factura"]]

    archivo_merge = archivo.merge(analisis_rollos, on ="Descripcion en factura" , how = "left")
    #---------------------------------------------------------------------------------------------------------------------
    archivo.to_excel(f"Salida/{version_lectura}/Match_Solr_New_Model_textos_procesados_match_Tiendas_TR_nuevo_ph_v{version_lectura}.xlsx", index=None)
    archivo_merge.to_excel(f"Salida/{version_lectura}/Match_Solr_New_Model_textos_procesados_match_Tiendas_TR_nuevo_ph_v{version_lectura}.xlsx", index=None)
    return archivo
#---------------------------------------------------------------------------------------------------------------------