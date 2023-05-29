import os
import meilisearch
ruta_imagenes ='Sin Codificar'
folder_to_proccess =  os.listdir(ruta_imagenes)
model_id= "347e4971-65d2-4c4b-bac8-9b5b3634e28c"
url_nanonets = f'https://app.nanonets.com/api/v2/OCR/Model/{model_id}/LabelFile/'
api_key = 'MvG6bWZujIeylTY_ofJqSiU--FjK-05D'

client = meilisearch.Client('http://44.192.93.228', '8ddc615c-a915-4d0f-9abb-c77d87e0d733')
url_solr = "http://44.192.93.228:8983/solr/tienda/query"
replaces = {"PH":"PAPEL","COMPLET":"COMPLETO","COMPLETOO":"COMPLETO",
            "DESINF":"DESINFECTANTE","ULT":"ULTRA","COLG":"COLGATE","EXT":"EXTRA","FABUL":"FABULOSO", "ALT":"ALTERNATIVA","HIG":"HIGIENICO",
            "CUID":"CUIDADO","DOB":"DOBLE","COMP":"COMPLETO","PEQ":"PEQUEÑO","PARRI":"PARRILLA","DESMANCH": "DESMANCHADOR","JAB":"JABON"}
unidades_medida = ["GRAMOS", "GR","G","LITROS", "LT", "L", "WATTS", "W", "MILILITROS","ML","METROS", "MTS","M" ,"UND" "CENTIMETROS", "CM"]
separador_unidades = ["X[0-9]+"]
separador_unidades.append("[0-9]+" + f"({'|'.join(unidades_medida)})")
min_len_word = 2
stop_words_contains=["(" ,")" ,"[" ,"]","GRTS", "BONIF","PPK","GRT","CJJ","DESCRIPCIÓN"]
palabras_bonificacion =["GTS","GTR", "GRTS","GRATIS","BONIF","BONI","PAGUE","LLEVE","OBSEQUIO","OFERTA","OFER","+","PG","LLV","PAG","GT","OFT","Bonificacion","OFE"]
contenedores = {"codigo_producto":["CODIGO", "LINEAS"], "descripcion":["PRODUCTO", "DESCRIPCION", "SERVICIO", "ARTICULO","DESCRIPCIÓN"], "cantidad":["CANT"]}
replace_distribuidores = { "DRYPERS" : "DRYPERS ANDINA S.A", "COLOMBIANA KIMBERLY COLPAPEL" : "COLOMBIANA KIMBERLY COLPAPEL", "Dist Distritiendas De Occidente" :"DISTRITIENDAS DE OCCIDENTE",
                           "Distr Distritiendas De Occidente" : "DISTRITIENDAS DE OCCIDENTE", "Distritien Distritiendas De Occidente8002221.39-7": "DISTRITIENDAS DE OCCIDENTE",
                           "Distritiendas De Occidente" : "DISTRITIENDAS DE OCCIDENTE", "Distritiendas De Occidente ," : "DISTRITIENDAS DE OCCIDENTE",
                           "Distritiendas Distritiendas De Occidente" : "DISTRITIENDAS DE OCCIDENTE", "Distritieng Distritiendas De Occidente ,":"DISTRITIENDAS DE OCCIDENTE",
                           "Spi Distritiendas De Occidente" : "DISTRITIENDAS DE OCCIDENTE", "Distritiendas DISTRITIENDAS DE OCCIDENTE" : "DISTRITIENDAS DE OCCIDENTE",
                           "Distritieng DISTRITIENDAS DE OCCIDENTE ," : "DISTRITIENDAS DE OCCIDENTE", "DISTRITIENDAS DE OCCIDENTE ," : "DISTRITIENDAS DE OCCIDENTE",
                           "DISTRITIEN TIENDAS DE OCCIDENTE": "DISTRITIENDAS DE OCCIDENTE", "DISTRITIENDAS DE OCCIDENTE 800222159-7" : "DISTRITIENDAS DE OCCIDENTE",
                           "DISTRIVARIOS Y VARIOS S.A.S. NIT : 901527899-5" : "DISTRITIENDAS DE OCCIDENTE", "SOFTWARE SIESA S.A." :"DISTRITIENDAS DE OCCIDENTE",
                           "Su Distritiendas De Occidente" : "DISTRITIENDAS DE OCCIDENTE" , "Distribuidora dH HOYOS2008 S.A.": "DISTRIBUIDORA HOYOS S.A.",
                           "Distribuidora HOYOS2008 S.A." : "DISRIBUIDORA HOYOS S.A." , "PANDAPAN DISTRIBUCIONES S.A.S" : "PANDAPAN DISTRIBUCIONES S.A.S.",
                           "PANDAPAN DISTRIBUCIONES S.A.STEL .": "PANDAPAN DISTRIBUCIONES S.A.S.","SPI DISTRITIENDAS DE OCCIDENTE" : "DISTRITIENDAS DE OCCIDENTE",
                           "SU DISTRITIENDAS DE OCCIDENTE" : "DISTRITIENDAS DE OCCIDENTE" ,"DISTRIJASS CIA S.A.S NIT":"DISTRIJASS CIA S.A.S" ,
                           "COMERCIALIZADORA Y DISTRIBUIDORA LA" : "COMERCIALIZADORA Y DISTRIBUIDORA LA TORRE SAS"
                        }
replace_codigo_factura = {
                            "FVE - ":"","POS":"","TXP":"","FR":"","FD ":""," - ":"","FLE ":"","HAS6.000":"","FV":"","HASG.000":"","POBQ":"","D":"","FCE ":"","NO.":"","C":""
                            ,"HASB.":"","MB":"","FE ":"","I ":"","FEL":"","T ":"","L ":"","FE":""
                         }

replace_iva_linea = {"%":"" , ".00":"", "* ":""}

ratio_lectura= 1
columnas_tabla = ["Precio", "cantidad", "codigo_producto", "descuento", "iva", "total", "unidad_medida","valor_unitario"]

version_lectura = "Consolidado182324mayo"