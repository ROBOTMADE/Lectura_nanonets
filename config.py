
import os
import meilisearch
ruta_imagenes ='NanonetsImagenes'
folder_to_proccess =  os.listdir(ruta_imagenes)
model_id= "347e4971-65d2-4c4b-bac8-9b5b3634e28c"
url_nanonets = f'https://app.nanonets.com/api/v2/OCR/Model/{model_id}/LabelFile/'
api_key = 'MvG6bWZujIeylTY_ofJqSiU--FjK-05D'

client = meilisearch.Client('http://localhost:7700')
url_solr = "http://44.192.93.228:8983/solr/tienda/query"
replaces = {"PH":"PAPEL","COMPLET":"COMPLETO","COMPLETOO":"COMPLETO",
            "DESINF":"DESINFECTANTE","ULT":"ULTRA","COLG":"COLGATE","EXT":"EXTRA","FABUL":"FABULOSO", "ALT":"ALTERNATIVA","HIG":"HIGIENICO",
            "CUID":"CUIDADO","DOB":"DOBLE","COMP":"COMPLETO","PEQ":"PEQUEÑO","PARRI":"PARRILLA","DESMANCH": "DESMANCHADOR"}
unidades_medida = ["GRAMOS", "GR","G","LITROS", "LT", "L", "WATTS", "W", "MILILITROS","ML","METROS", "MTS","M" ,"UND" "CENTIMETROS", "CM"]
separador_unidades = ["X[0-9]+"]
separador_unidades.append("[0-9]+" + f"({'|'.join(unidades_medida)})")
min_len_word = 2
stop_words_contains=["(" ,")" ,"[" ,"]","GRTS", "BONIF","PPK","GRT","CJJ"]

ratio_lectura= 0.0007

version_lectura = 2