import requests
import json
import pandas as pd
from tqdm import tqdm
import re
from config import *
potenciadores = "DONKAT"
def procesar(df):
    facturas = df
    codigos_barra = []
    descripciones_tr = []
    descripciones_mailsearch =[]
    codigos_barra_mailsearch =[]
    textos=[]
    ids=[]

    for index, row in tqdm(facturas.iterrows(), total= facturas.shape[0]):
            bandera_continuar= True
            if index == 5:
                print ()
            try:
                palabra_meilisearch = ""
                descripcion = row["descripcion"]
                palabras_descripcion= descripcion.split()
                query=""
            except Exception as e:
                codigos_barra_mailsearch.append("NO ENCONTRADO")
                descripciones_mailsearch.append("NO ENCONTRADO")
                codigos_barra.append("NO ENCONTRADO")
                descripciones_tr.append("NO ENCONTRADO")
                bandera_continuar = False
                textos.append(str(descripcion))

            if bandera_continuar:
                extends_check =False
                palabras_a_ordenar = []
                #palabras_a_ordenar = palabras_descripcion.copy()
                cantidad_palabras_cumplen =0
                palabras_carry = []
                for i, palabra in enumerate(palabras_descripcion):
                    if cantidad_palabras_cumplen == 2:
                        palabras_a_ordenar.append(palabra)
                    if cantidad_palabras_cumplen <2 and len(palabra)>2:
                        palabras_a_ordenar.append(palabra)
                        cantidad_palabras_cumplen +=1
                    if len(palabra) < 3 and cantidad_palabras_cumplen < 2:
                        palabras_carry.append(palabra)
                    if (i==len(palabras_descripcion)-1 or cantidad_palabras_cumplen == 2) and not extends_check:
                        palabras_a_ordenar.extend(palabras_carry)
                        extends_check = True

                descripcion_limpia = ' '.join(palabras_a_ordenar)

            
                # if len(palabra) < 3 and cantidad_palabras_cumplen < 3:
                #     palabras_a_ordenar.append(palabra)
                #     cantidad_palabras_cumplen +=1
                # elif cantidad_palabras_cumplen == 2:
                #     palabras_a_ordenar.extend(palabras_carry)
                # elif cantidad_palabras_cumplen < 3:
                #     palabras_carry.append(palabra)
                # else:
                #     palabras_a_ordenar.append(palabra)
                #     
                # descripcion_limpia = ' '.join(palabras_a_ordenar)
                
                for i , palabra in enumerate(descripcion_limpia.split()):
                    palabra_limpia = palabra.upper().strip()
                    for replace in replaces:
                        if palabra_limpia == replace:
                            palabra_limpia = replaces[replace]
                        #palabra_limpia=palabra_limpia.replace(replace, replaces[replace])
                    if not str(palabra_limpia).isnumeric():
                        for stop_word in stop_words_contains:
                            palabra_limpia = palabra_limpia.replace(stop_word, "")
                    else:
                        if len(palabras_descripcion) - 1 != i and not palabras_descripcion[i+1] in unidades_medida:
                            palabra_limpia = ""
                    for separador_unidad in separador_unidades:
                        try:
                            chars = re.findall(separador_unidad, palabra_limpia)
                            palabra_limpia = re.sub(chars[0], f' {chars[0]} ', palabra_limpia)
                        except Exception as e:
                            ...
                    if len(palabra_limpia) <= min_len_word and not palabra_limpia in (unidades_medida):
                        palabra_limpia = ""

                    if palabra_limpia != "":
                        palabra_limpia = palabra_limpia.strip()
                        palabra_meilisearch += palabra_limpia+" "
                        query += f'desc_long: "{palabra_limpia}", '
                try:
                    texto = palabra_meilisearch
                    #print (texto)
                    textos.append(texto)
                    response_mailisearch = client.index('TR_marzo').search(texto)
                    producto_mailisearch = response_mailisearch['hits'][0]
                    descripciones_mailsearch.append(producto_mailisearch['DescripcionLargaProducto'])
                    codigos_barra_mailsearch.append(producto_mailisearch['CodigoDeBarras'])
                except Exception as e:
                    #response_dict = json.loads(response.text)
                    # codigos_barra.append("NO ENCONTRADO")
                    # descripciones_tr.append("NO ENCONTRADO")
                    codigos_barra_mailsearch.append("NO ENCONTRADO")
                    descripciones_mailsearch.append("NO ENCONTRADO")
                try:
                    query = query[:-2]
                    payload={'q': query,
                    'indent': 'True',
                    'fl': 'idproduct, desc_long, score',
                    'q.op': 'OR'}
                    files=[]
                    headers = {}
                    response = requests.request("GET", url_solr, headers=headers, data=payload, files=files)
                    response_dict = json.loads(response.text)
                    productor = response_dict["response"]["docs"]
                    producto_similar = productor[0]
                    #codigos_barra.append(producto_similar['idproduct'])

                    descripciones_tr.append(producto_similar['desc_long'])
                    if codigos_barra_mailsearch[-1] == "NO ENCONTRADO":
                        codigos_barra_mailsearch[-1] = producto_similar['idproduct']
                        descripciones_mailsearch[-1] =producto_similar['desc_long']
                except Exception as e:
                    # response_dict = json.loads(response.text)
                    codigos_barra.append("NO ENCONTRADO")
                    descripciones_tr.append("NO ENCONTRADO")
                    # codigos_barra_mailsearch.append("NO ENCONTRADO")
                    # descripciones_mailsearch.append("NO ENCONTRADO")
            ruta_imagen = row["ruta_factura"]
            try:
                expresion = "ID [0-9]+"
                chars = re.findall(expresion, ruta_imagen)[0]
                id = chars.split()[1]
            except:
                try:
                    expresion = "CC[0-9]+"
                    chars = re.findall(expresion, ruta_imagen)[0]
                    id = chars.replace("CC","")
                except:
                    try:
                        expresion = "ID[0-9]+"
                        chars = re.findall(expresion, ruta_imagen)[0]
                        id = chars.replace("ID", "")
                    except:
                        try:
    
                            expresion = "VP[0-9]+"
                            chars = re.findall(expresion, ruta_imagen)[0]
                            id = chars.replace("VP","")
                            
                        except:
                            try:
                                expresions = "CC [0-9]+"
                                chars = re.findall(expresion, ruta_imagen)[0]
                                id = chars.split()[1]
                            except:
                                    id="0"
                            ids.append(int(id))

    facturas["texto_procesado"] = textos
    facturas["ID"] = ids
    facturas["CodigoDeBarras"] = codigos_barra_mailsearch
    facturas["descripcion_solr"] = descripciones_tr
    facturas["descripcion_mailisearch"] = descripciones_mailsearch
    facturas["codigoBarra_mailisearch"] = codigos_barra_mailsearch

    maestro_tiendas = pd.read_excel("Base de tiendas activas Tienda Registrada.xlsx", index_col=None)
    consolidado = pd.merge(facturas ,maestro_tiendas, on ="ID", how="left")
    
    consolidado.to_excel(f"Salida/{version_lectura}/etapa1.xlsx",
                         index=None)

    #consolidado = pd.read_excel(f"Salida/{version_lectura}/etapa1.xlsx",
    #                     index_col=None)
    #################################################################################################
    productos =  pd.read_csv("Maestro_TR_2_marzo_lite.csv", sep =";", encoding="iso8859-1")
    productos = productos[["Categoria", "SubCategoria", "marca", "CodigoDeBarras","NombreDeProductor"]]
    productos["CodigoDeBarras"]= productos["CodigoDeBarras"].astype(str)
    consolidado["CodigoDeBarras"] = consolidado["CodigoDeBarras"].astype(str)
    archivo_merge = consolidado.merge(productos, on="CodigoDeBarras", how="left")
    archivo_merge.rename(columns={"CodigoDeBarras":"codigoBarra_solr"}, inplace=True)
    #archivo_merge = archivo_merge[["Categoria", "SubCategoria", "marca", ""]]
    #################################################################################################
    consolidado.to_excel(f"Salida/{version_lectura}/Match_Solr_New_Model_textos_procesados_match_Tiendas_TR.xlsx", index=None)
    archivo_merge.to_excel(f"Salida/{version_lectura}/data_final.xlsx", index=None)
    return archivo_merge